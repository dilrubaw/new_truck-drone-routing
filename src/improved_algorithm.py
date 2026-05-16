import random
import math
import time
from pathlib import Path
import pandas as pd

from initial_solution import create_initial_solution
from dijkstra_sync import build_solution_with_sync
from evaluator import evaluate_solution
from distance_matrix import compute_distance_matrix
from or_opt import or_opt


def route_distance(route, distance_matrix):
    total = 0.0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]
    return total


def random_destruction(route):
    if len(route) <= 4:
        return route[:]

    start_node = route[0]
    end_node = route[-1]
    middle = route[1:-1]

    if len(middle) <= 2:
        return route[:]

    start = random.randint(0, len(middle) - 2)
    end = random.randint(start + 1, min(start + 4, len(middle)))

    removed = middle[start:end]
    remaining = middle[:start] + middle[end:]

    insert_pos = random.randint(0, len(remaining))
    new_middle = remaining[:insert_pos] + removed[::-1] + remaining[insert_pos:]

    return [start_node] + new_middle + [end_node]


def worst_position_destruction(route, instance, remove_count=3):
    if len(route) <= 4:
        return route[:]

    distance_matrix = compute_distance_matrix(instance)

    start_node = route[0]
    end_node = route[-1]
    middle = route[1:-1]

    if len(middle) <= remove_count:
        return random_destruction(route)

    contributions = []

    for i in range(1, len(route) - 1):
        prev_node = route[i - 1]
        node = route[i]
        next_node = route[i + 1]

        marginal_cost = (
            distance_matrix[prev_node][node]
            + distance_matrix[node][next_node]
            - distance_matrix[prev_node][next_node]
        )

        contributions.append((marginal_cost, node))

    contributions.sort(reverse=True)
    removed_nodes = {node for _, node in contributions[:remove_count]}

    remaining_middle = [node for node in middle if node not in removed_nodes]
    removed = [node for node in middle if node in removed_nodes]

    insert_pos = random.randint(0, len(remaining_middle))
    new_middle = (
        remaining_middle[:insert_pos]
        + removed
        + remaining_middle[insert_pos:]
    )

    return [start_node] + new_middle + [end_node]


def zone_based_destruction(route, instance, remove_count=3):
    if len(route) <= 4:
        return route[:]

    start_node = route[0]
    end_node = route[-1]
    middle = route[1:-1]

    if len(middle) <= remove_count:
        return random_destruction(route)

    distance_matrix = compute_distance_matrix(instance)

    seed_node = random.choice(middle)

    nearest_nodes = sorted(
        middle,
        key=lambda node: distance_matrix[seed_node][node]
    )[:remove_count]

    removed_set = set(nearest_nodes)
    remaining_middle = [node for node in middle if node not in removed_set]
    removed = [node for node in middle if node in removed_set]

    insert_pos = random.randint(0, len(remaining_middle))
    new_middle = (
        remaining_middle[:insert_pos]
        + removed[::-1]
        + remaining_middle[insert_pos:]
    )

    return [start_node] + new_middle + [end_node]


def select_operator(operator_weights):
    operators = list(operator_weights.keys())
    weights = list(operator_weights.values())
    return random.choices(operators, weights=weights, k=1)[0]


def update_operator_weights(operator_weights, selected_operator, improved, reward=0.10):
    if improved:
        operator_weights[selected_operator] += reward
    else:
        operator_weights[selected_operator] *= 0.99

    total = sum(operator_weights.values())

    for operator in operator_weights:
        operator_weights[operator] /= total

    return operator_weights


def adaptive_cooling(
    temperature,
    base_cooling_rate,
    no_improvement_counter,
    stagnation_limit
):
    if no_improvement_counter >= stagnation_limit:
        cooling_rate = 0.995
    else:
        cooling_rate = base_cooling_rate

    return temperature * cooling_rate


def acceptance_probability(current_cost, candidate_cost, temperature):
    if candidate_cost < current_cost:
        return 1.0

    if temperature <= 0:
        return 0.0

    return math.exp(-(candidate_cost - current_cost) / temperature)


def apply_adaptive_destruction(route, instance, operator):
    if operator == "random":
        return random_destruction(route)

    if operator == "worst_position":
        return worst_position_destruction(route, instance)

    if operator == "zone_based":
        return zone_based_destruction(route, instance)

    raise ValueError(f"Unknown destruction operator: {operator}")


def hybrid_ig_sa(
    instance,
    max_iterations=300,
    initial_temperature=100.0,
    base_cooling_rate=0.95,
    stagnation_limit=30,
    time_limit_seconds=30
):
    start_time = time.time()

    current_solution = create_initial_solution(instance)
    current_result = evaluate_solution(instance, current_solution)
    current_cost = current_result["penalized_objective"]

    best_solution = current_solution
    best_result = current_result
    best_cost = current_cost

    temperature = initial_temperature
    no_improvement_counter = 0

    operator_weights = {
        "random": 1 / 3,
        "worst_position": 1 / 3,
        "zone_based": 1 / 3
    }

    history = []

    for iteration in range(1, max_iterations + 1):
        if time.time() - start_time > time_limit_seconds:
            break

        selected_operator = select_operator(operator_weights)

        destroyed_route = apply_adaptive_destruction(
            current_solution.node_sequence,
            instance,
            selected_operator
        )

        improved_route = or_opt(destroyed_route, instance)

        candidate_solution = build_solution_with_sync(
            instance,
            improved_route
        )

        candidate_result = evaluate_solution(instance, candidate_solution)
        candidate_cost = candidate_result["penalized_objective"]

        improved = candidate_cost < best_cost

        probability = acceptance_probability(
            current_cost,
            candidate_cost,
            temperature
        )

        if random.random() < probability:
            current_solution = candidate_solution
            current_result = candidate_result
            current_cost = candidate_cost

        if improved:
            best_solution = candidate_solution
            best_result = candidate_result
            best_cost = candidate_cost
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        operator_weights = update_operator_weights(
            operator_weights,
            selected_operator,
            improved
        )

        temperature = adaptive_cooling(
            temperature,
            base_cooling_rate,
            no_improvement_counter,
            stagnation_limit
        )

        history.append({
            "iteration": iteration,
            "current_cost": current_cost,
            "candidate_cost": candidate_cost,
            "best_cost": best_cost,
            "temperature": temperature,
            "selected_operator": selected_operator,
            "random_weight": operator_weights["random"],
            "worst_position_weight": operator_weights["worst_position"],
            "zone_based_weight": operator_weights["zone_based"],
            "feasible": candidate_result["feasible"]
        })

    return best_solution, best_result, history


if __name__ == "__main__":
    from data_loader import load_bouman_instance

    instance_path = Path("data/singlecenter/singlecenter-61-n20.txt")
    instance = load_bouman_instance(instance_path)

    best_solution, best_result, history = hybrid_ig_sa(instance)

    print("Instance:", instance.name)
    print("Node count:", len(instance.nodes))
    print("Best node sequence:")
    print(best_solution.node_sequence)
    print("Best resource types:")
    print(best_solution.resource_types)
    print("Best result:")
    print(best_result)

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    result_df = pd.DataFrame([{
        "algorithm": "Hybrid IG-SA",
        "instance": instance.name,
        "node_count": len(instance.nodes),
        "makespan": best_result["makespan"],
        "penalized_objective": best_result["penalized_objective"],
        "feasible": best_result["feasible"],
        "battery_capacity": best_result["battery_capacity"],
        "total_battery_violation": best_result["total_battery_violation"],
        "alpha": best_result["alpha"]
    }])

    result_path = results_dir / "hybrid_ig_sa_result.csv"
    result_df.to_csv(result_path, index=False)

    history_df = pd.DataFrame(history)
    history_path = results_dir / "hybrid_ig_sa_history.csv"
    history_df.to_csv(history_path, index=False)

    print(f"Saved hybrid result to: {result_path}")
    print(f"Saved hybrid convergence history to: {history_path}")