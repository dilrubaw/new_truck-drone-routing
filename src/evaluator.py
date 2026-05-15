from models import ProblemInstance, Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def path_time(path, time_matrix):
    total = 0.0

    for i in range(len(path) - 1):
        total += time_matrix[path[i]][path[i + 1]]

    return total


def evaluate_solution(instance: ProblemInstance, solution: Solution) -> dict:
    truck_time_matrix = compute_truck_time_matrix(instance)
    drone_time_matrix = compute_drone_time_matrix(instance)

    seq = solution.node_sequence
    types = solution.resource_types

    if len(seq) != len(types):
        raise ValueError("node_sequence and resource_types must have same length.")

    if types[0] != 0 or types[-1] != 0:
        raise ValueError("First and last nodes must be synchronization nodes with type 0.")

    sync_positions = [
        i for i, resource_type in enumerate(types)
        if resource_type == 0
    ]

    total_makespan = 0.0
    feasible = True
    violations = []

    for segment_index in range(len(sync_positions) - 1):
        start_pos = sync_positions[segment_index]
        end_pos = sync_positions[segment_index + 1]

        segment_nodes = seq[start_pos:end_pos + 1]
        segment_types = types[start_pos:end_pos + 1]

        truck_path = [segment_nodes[0]]
        drone_path = [segment_nodes[0]]

        for node, resource_type in zip(segment_nodes[1:-1], segment_types[1:-1]):
            if resource_type == 1:
                drone_path.append(node)
            elif resource_type == 2:
                truck_path.append(node)
            elif resource_type == 0:
                truck_path.append(node)
                drone_path.append(node)

        truck_path.append(segment_nodes[-1])
        drone_path.append(segment_nodes[-1])

        truck_segment_time = path_time(truck_path, truck_time_matrix)
        drone_segment_time = path_time(drone_path, drone_time_matrix)

        if drone_segment_time > instance.battery_capacity:
            feasible = False
            violations.append({
                "segment": segment_index + 1,
                "from_node": segment_nodes[0],
                "to_node": segment_nodes[-1],
                "drone_time": float(drone_segment_time),
                "battery_capacity": float(instance.battery_capacity)
            })

        total_makespan += max(truck_segment_time, drone_segment_time)

    return {
        "makespan": float(total_makespan),
        "feasible": feasible,
        "battery_capacity": float(instance.battery_capacity),
        "violations": violations
    }