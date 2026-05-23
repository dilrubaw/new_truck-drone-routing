from models import Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def build_solution_with_sync(instance, route):
    truck_time_matrix = compute_truck_time_matrix(instance)
    drone_time_matrix = compute_drone_time_matrix(instance)

    resource_types = [0 for _ in route]

    last_sync_index = 0
    resource_types[0] = 0
    resource_types[-1] = 0

    for i in range(1, len(route) - 1):
        start_node = route[last_sync_index]
        current_node = route[i]
        next_node = route[i + 1]

        drone_path = route[last_sync_index:i + 1]

        drone_time = 0.0

        for j in range(len(drone_path) - 1):
            drone_time += drone_time_matrix[
                drone_path[j]
            ][
                drone_path[j + 1]
            ]

        drone_time += drone_time_matrix[current_node][next_node]

        truck_time = truck_time_matrix[start_node][next_node]

        if drone_time <= instance.battery_capacity:
            resource_types[i] = 1
        else:
            resource_types[i] = 0
            last_sync_index = i
            
    resource_types[-1] = 0

    sync_count = sum(1 for resource_type in resource_types if resource_type == 0)

    if sync_count <= 2 and len(route) > 3:
        middle_index = len(route) // 2
        resource_types[middle_index] = 0

    return Solution(
        node_sequence=route,
        resource_types=resource_types
    )