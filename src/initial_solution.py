from two_opt import nearest_neighbor_route, two_opt
from or_opt import or_opt
from dijkstra_sync import build_solution_with_sync


def create_initial_solution(instance):
    route = nearest_neighbor_route(instance)

    improved_route = two_opt(
        route,
        instance,
        max_iterations=100
    )

    improved_route = or_opt(
        improved_route,
        instance,
        max_segment_size=3
    )

    solution = build_solution_with_sync(
        instance,
        improved_route
    )

    return solution