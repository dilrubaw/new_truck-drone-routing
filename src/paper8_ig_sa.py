import random
import math
import time

from initial_solution import create_initial_solution
from dijkstra_sync import build_solution_with_sync
from evaluator import evaluate_solution


def destroy_and_reconstruct(route):
    """
    Origin and end nodes are fixed.
    Only middle customer nodes are changed.
    """

    if len(route) <= 4:
        return route[:]

    start_node = route[0]
    end_node = route[-1]
    middle = route[1:-1]

    if len(middle) <= 2:
        return route[:]

    start = random.randint(0, len(middle) - 2)
    end = random.randint(start + 1, min(start + 4, len(middle)))

    segment = middle[start:end]
    remaining = middle[:start] + middle[end:]

    insert_pos = random.randint(0, len(remaining))

    new_middle = (
        remaining[:insert_pos]
        + segment[::-1]
        + remaining[insert_pos:]
    )

    return [start_node] + new_middle + [end_node]

def acceptance_probability(current_cost, new_cost, temperature):
    """
    Simulated Annealing acceptance criterion.
    Daha iyi çözüm her zaman kabul edilir.
    Daha kötü çözüm belirli olasılıkla kabul edilir.
    """

    if new_cost < current_cost:
        return 1.0

    if temperature <= 0:
        return 0.0

    return math.exp(-(new_cost - current_cost) / temperature)


def paper8_ig_sa(
    instance,
    max_iterations=300,
    initial_temperature=100.0,
    cooling_rate=0.95,
    time_limit_seconds=30
):
    """
    Paper 8 baseline için Iterated Greedy + Simulated Annealing.
    """

    start_time = time.time()

    current_solution = create_initial_solution(instance)
    current_result = evaluate_solution(instance, current_solution)
    current_cost = current_result["penalized_objective"]

    best_solution = current_solution
    best_result = current_result
    best_cost = current_cost

    temperature = initial_temperature

    history = []

    for iteration in range(1, max_iterations + 1):
        if time.time() - start_time > time_limit_seconds:
            break

        candidate_route = destroy_and_reconstruct(
            current_solution.node_sequence
        )

        candidate_solution = build_solution_with_sync(
            instance,
            candidate_route
        )

        candidate_result = evaluate_solution(
            instance,
            candidate_solution
        )

        candidate_cost = candidate_result["penalized_objective"]

        probability = acceptance_probability(
            current_cost,
            candidate_cost,
            temperature
        )

        if random.random() < probability:
            current_solution = candidate_solution
            current_result = candidate_result
            current_cost = candidate_cost

        if candidate_cost < best_cost:
            best_solution = candidate_solution
            best_result = candidate_result
            best_cost = candidate_cost

        history.append({
            "iteration": iteration,
            "current_cost": current_cost,
            "candidate_cost": candidate_cost,
            "best_cost": best_cost,
            "temperature": temperature,
            "feasible": candidate_result["feasible"]
        })

        temperature *= cooling_rate

    return best_solution, best_result, history