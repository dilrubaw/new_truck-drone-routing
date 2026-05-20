from two_opt import route_distance
from distance_matrix import compute_distance_matrix


def or_opt(route, instance, evaluator=None, max_segment_size=3):
    """
    Or-Opt local search.
    Relocates segments of 1, 2, or 3 nodes to another position.
    Origin and end nodes remain fixed.

    evaluator parameter is optional for compatibility.
    """

    if len(route) <= 4:
        return route[:]

    distance_matrix = compute_distance_matrix(instance)

    best_route = route[:]
    best_distance = route_distance(best_route, distance_matrix)

    improved = True

    while improved:
        improved = False

        for segment_size in range(1, max_segment_size + 1):
            for i in range(1, len(best_route) - segment_size):
                segment = best_route[i:i + segment_size]
                remaining = best_route[:i] + best_route[i + segment_size:]

                for j in range(1, len(remaining)):
                    if j == i:
                        continue

                    new_route = (
                        remaining[:j]
                        + segment
                        + remaining[j:]
                    )

                    new_distance = route_distance(new_route, distance_matrix)

                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break

                if improved:
                    break

            if improved:
                break

    return best_route