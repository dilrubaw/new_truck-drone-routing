import heapq

from models import Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def cumulative_drone_time(route, start_pos, end_pos, drone_matrix):
    """
    Computes cumulative drone travel time between two synchronization positions
    along the given TSP route.

    Example:
    route = [0, 5, 2, 8, 9]
    start_pos = 0
    end_pos = 3

    Drone path:
    0 -> 5 -> 2 -> 8
    """

    total = 0.0

    for pos in range(start_pos, end_pos):
        current_node = route[pos]
        next_node = route[pos + 1]
        total += drone_matrix[current_node][next_node]

    return total


def build_dijkstra_graph(instance, route):
    """
    Builds the auxiliary Dijkstra graph described in Paper 8 Algorithm 2.

    Each position in the TSP route is treated as a node in this auxiliary graph.

    Edge i -> j exists only if the drone can travel from route[i] to route[j]
    through all intermediate nodes without exceeding battery capacity Q.

    Edge cost:
        cost(i, j) = max(truck_time(route[i], route[j]),
                         cumulative_drone_time(route[i] ... route[j]))

    Constraint:
        cumulative_drone_time <= Q
    """

    truck_matrix = compute_truck_time_matrix(instance)
    drone_matrix = compute_drone_time_matrix(instance)

    n = len(route)
    graph = {i: [] for i in range(n)}

    for i in range(n - 1):
        for j in range(i + 1, n):
            start_node = route[i]
            end_node = route[j]

            truck_time = truck_matrix[start_node][end_node]

            drone_time = cumulative_drone_time(
                route,
                i,
                j,
                drone_matrix
            )

            if drone_time <= instance.battery_capacity:
                edge_cost = max(truck_time, drone_time)
                graph[i].append((j, edge_cost))

    return graph


def run_dijkstra(graph, start_pos, end_pos):
    distances = {
        node: float("inf")
        for node in graph
    }

    previous = {
        node: None
        for node in graph
    }

    distances[start_pos] = 0.0

    priority_queue = [(0.0, start_pos)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end_pos:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_cost in graph[current_node]:
            new_distance = current_distance + edge_cost

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return distances, previous


def extract_sync_positions(previous, end_pos):
    sync_positions = set()

    current = end_pos

    while current is not None:
        sync_positions.add(current)
        current = previous[current]

    return sync_positions


def build_solution_with_sync(instance, route):
    """
    Converts a TSP route pi_s into a synchronized truck-drone solution pi_t.

    pi_s:
        Node sequence.

    pi_t:
        Resource type sequence:
        0 = truck + drone synchronization node
        1 = drone-only node
        2 = truck-only node

    In this baseline construction:
        - Synchronization nodes are selected by Dijkstra.
        - Intermediate nodes between synchronization points are assigned to drone.
        - Truck moves directly between synchronization nodes.
    """

    n = len(route)

    graph = build_dijkstra_graph(instance, route)

    distances, previous = run_dijkstra(
        graph,
        start_pos=0,
        end_pos=n - 1
    )

    if distances[n - 1] == float("inf"):
        sync_positions = {0, n - 1}
    else:
        sync_positions = extract_sync_positions(
            previous,
            end_pos=n - 1
        )

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