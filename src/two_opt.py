from distance_matrix import compute_distance_matrix


def route_distance(route, distance_matrix):
    total = 0.0

    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]

    return total


def nearest_neighbor_route(instance):
    distance_matrix = compute_distance_matrix(instance)

    n = len(instance.nodes)
    unvisited = set(range(1, n))

    route = [0]
    current = 0

    while unvisited:
        next_node = min(
            unvisited,
            key=lambda node: distance_matrix[current][node]
        )

        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    return route


def two_opt(route, instance, max_iterations=100):
    distance_matrix = compute_distance_matrix(instance)

    best_route = route[:]
    best_distance = route_distance(best_route, distance_matrix)

    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                new_route = (
                    best_route[:i]
                    + best_route[i:j + 1][::-1]
                    + best_route[j + 1:]
                )

                new_distance = route_distance(new_route, distance_matrix)

                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True

    return best_route