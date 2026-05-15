import heapq

from models import Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def drone_subroute_time(route, start_pos, end_pos, drone_matrix):
    total = 0.0

    for i in range(start_pos, end_pos):
        current_node = route[i]
        next_node = route[i + 1]
        total += drone_matrix[current_node][next_node]

    return total


def build_solution_with_sync(instance, route):
    """
    Route üzerinden sync noktalarını seçer.
    Mantık:
    - Sync node = type 0
    - Sync node arası müşteriler drone-only = type 1
    - Truck sync noktaları arasında direkt gider
    """

    n = len(route)

    truck_matrix = compute_truck_time_matrix(instance)
    drone_matrix = compute_drone_time_matrix(instance)

    battery_capacity = instance.battery_capacity

    graph = {i: [] for i in range(n)}

    for i in range(n - 1):
        for j in range(i + 1, n):
            start_node = route[i]
            end_node = route[j]

            drone_time = drone_subroute_time(
                route,
                i,
                j,
                drone_matrix
            )

            truck_time = truck_matrix[start_node][end_node]

            if drone_time <= battery_capacity:
                segment_cost = max(truck_time, drone_time)
                graph[i].append((j, segment_cost))

    distances = [float("inf")] * n
    previous = [None] * n

    distances[0] = 0.0

    pq = [(0.0, 0)]

    while pq:
        current_distance, current_pos = heapq.heappop(pq)

        if current_distance > distances[current_pos]:
            continue

        for next_pos, cost in graph[current_pos]:
            new_distance = current_distance + cost

            if new_distance < distances[next_pos]:
                distances[next_pos] = new_distance
                previous[next_pos] = current_pos
                heapq.heappush(pq, (new_distance, next_pos))

    sync_positions = set()

    if previous[n - 1] is None:
        # fallback: only origin and end are synchronization nodes
        sync_positions.add(0)
        sync_positions.add(n - 1)
    else:
        current = n - 1

        while current is not None:
            sync_positions.add(current)
            current = previous[current]

        sync_positions.add(0)
        sync_positions.add(n - 1)

    resource_types = []

    for pos in range(n):
        if pos in sync_positions:
            resource_types.append(0)
        else:
            resource_types.append(1)

    return Solution(
        node_sequence=route,
        resource_types=resource_types
    )