import random
import math
import time

from initial_solution import create_initial_solution
from greedy_sync_builder import build_solution_with_sync
from evaluator import evaluate_solution
from or_opt import or_opt
from paper8_ig_sa import paper8_ig_sa

from adaptive_destruction import (
    random_destruction,
    worst_position_destruction,
    zone_based_destruction,
    reconstruct_route,
    select_operator,
    update_operator_weights
)

from adaptive_cooling import adaptive_cooling


def choose_better_solution(instance, route_a, route_b):
    solution_a = build_solution_with_sync(instance, route_a)
    result_a = evaluate_solution(instance, solution_a)

    solution_b = build_solution_with_sync(instance, route_b)
    result_b = evaluate_solution(instance, solution_b)

    if result_b["penalized_objective"] < result_a["penalized_objective"]:
        return route_b, solution_b, result_b

    return route_a, solution_a, result_a


def hybrid_ig_sa(
    instance,
    max_iterations=2000,
    initial_temperature=500.0,
    base_cooling_rate=0.995,
    stagnation_limit=50,
    time_limit_seconds=60
):
    start_time = time.time()

    baseline_solution, baseline_result, _ = paper8_ig_sa(
        instance,
        max_iterations=1000,
        initial_temperature=500.0,
        cooling_rate=0.995,
        time_limit_seconds=min(30, time_limit_seconds)
    )

    initial_solution = create_initial_solution(instance)
    initial_result = evaluate_solution(instance, initial_solution)

    if baseline_result["penalized_objective"] <= initial_result["penalized_objective"]:
        current_solution = baseline_solution
        current_result = baseline_result
    else:
        current_solution = initial_solution
        current_result = initial_result

    current_cost = current_result["penalized_objective"]

    best_solution = current_solution
    best_result = current_result
    best_cost = current_cost

    temperature = initial_temperature

    weights = [1 / 3, 1 / 3, 1 / 3]
    scores = [0, 0, 0]
    counts = [0, 0, 0]

    no_improve_count = 0
    history = []

    for iteration in range(1, max_iterations + 1):
        if time.time() - start_time > time_limit_seconds:
            break

        operator_idx = select_operator(weights)
        counts[operator_idx] += 1

        route = current_solution.node_sequence

        if operator_idx == 0:
            remaining, removed = random_destruction(route)
            operator_name = "random"
        elif operator_idx == 1:
            remaining, removed = worst_position_destruction(route, instance)
            operator_name = "worst_position"
        else:
            remaining, removed = zone_based_destruction(route, instance)
            operator_name = "zone_based"

        reconstructed_route = reconstruct_route(remaining, removed)

        or_opt_route = or_opt(reconstructed_route, instance)

        candidate_route, candidate_solution, candidate_result = choose_better_solution(
            instance,
            reconstructed_route,
            or_opt_route
        )

        candidate_cost = candidate_result["penalized_objective"]
        delta = candidate_cost - current_cost

        accepted = False
        improved_best = False

        if candidate_cost < current_cost:
            accepted = True
        elif temperature > 0 and random.random() < math.exp(-delta / temperature):
            accepted = True

        if accepted:
            current_solution = candidate_solution
            current_result = candidate_result
            current_cost = candidate_cost

        if candidate_cost < best_cost:
            best_solution = candidate_solution
            best_result = candidate_result
            best_cost = candidate_cost
            scores[operator_idx] += 3
            no_improve_count = 0
            improved_best = True
        else:
            no_improve_count += 1

        if accepted and not improved_best:
            scores[operator_idx] += 1

        if iteration % 100 == 0:
            weights = update_operator_weights(weights, scores, counts)
            scores = [0, 0, 0]
            counts = [0, 0, 0]

        temperature = adaptive_cooling(
            temperature,
            base_cooling_rate,
            no_improve_count,
            threshold=stagnation_limit
        )

        history.append({
            "iteration": iteration,
            "current_cost": current_cost,
            "candidate_cost": candidate_cost,
            "best_cost": best_cost,
            "temperature": temperature,
            "selected_operator": operator_name,
            "random_weight": weights[0],
            "worst_position_weight": weights[1],
            "zone_based_weight": weights[2],
            "feasible": candidate_result["feasible"]
        })

    return best_solution, best_result, history