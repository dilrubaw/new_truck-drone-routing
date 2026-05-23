from two_opt import nearest_neighbor_route, two_opt
from greedy_sync_builder import build_solution_with_sync
from or_opt import or_opt
from distance_matrix import compute_distance_matrix


def create_initial_solution(instance):
    route = nearest_neighbor_route(instance)

    distance_matrix = compute_distance_matrix(instance)

    improved_route = two_opt(
        route,
        distance_matrix
    )

    improved_route = or_opt(
        improved_route,
        instance
    )

    solution = build_solution_with_sync(
        instance,
        improved_route
    )

    return solution