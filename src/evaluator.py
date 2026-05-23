from models import Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


EPSILON = 1e-9


def path_time(path, time_matrix):
    total = 0.0

    for i in range(len(path) - 1):
        total += time_matrix[path[i]][path[i + 1]]

    return total


def validate_solution(instance, solution: Solution):
    seq = solution.node_sequence
    types = solution.resource_types

    if len(seq) != len(types):
        raise ValueError("node_sequence and resource_types must have the same length.")

    if len(seq) < 2:
        raise ValueError("Solution must contain at least origin and destination nodes.")

    if types[0] != 0 or types[-1] != 0:
        raise ValueError("First and last nodes must be synchronization nodes.")

    for resource_type in types:
        if resource_type not in [0, 1, 2]:
            raise ValueError("Resource types must be 0, 1, or 2.")

    expected_nodes = sorted(node.id for node in instance.nodes)

    if sorted(seq) != expected_nodes:
        raise ValueError("node_sequence must contain each node exactly once.")

    if seq[0] != expected_nodes[0]:
        raise ValueError("node_sequence must start with the origin node.")

    if seq[-1] != expected_nodes[-1]:
        raise ValueError("node_sequence must end with the destination node.")


def evaluate_solution(instance, solution: Solution):
    validate_solution(instance, solution)

    truck_time_matrix = compute_truck_time_matrix(instance)
    drone_time_matrix = compute_drone_time_matrix(instance)

    seq = solution.node_sequence
    types = solution.resource_types

    sync_positions = [
        i for i, resource_type in enumerate(types)
        if resource_type == 0
    ]

    total_makespan = 0.0
    feasible = True
    violations = []
    total_battery_violation = 0.0

    segment_details = []

    for segment_index in range(len(sync_positions) - 1):
        start_pos = sync_positions[segment_index]
        end_pos = sync_positions[segment_index + 1]

        segment_nodes = seq[start_pos:end_pos + 1]
        segment_types = types[start_pos:end_pos + 1]

        start_node = segment_nodes[0]
        end_node = segment_nodes[-1]

        truck_path = [start_node]
        drone_path = [start_node]

        has_drone_flight = False

        for node, resource_type in zip(segment_nodes[1:-1], segment_types[1:-1]):
            if resource_type == 1:
                drone_path.append(node)
                has_drone_flight = True
            elif resource_type == 2:
                truck_path.append(node)
            elif resource_type == 0:
                truck_path.append(node)
                drone_path.append(node)
                has_drone_flight = True

        truck_path.append(end_node)
        truck_segment_time = path_time(truck_path, truck_time_matrix)

        if has_drone_flight:
            drone_path.append(end_node)
            drone_segment_time = path_time(drone_path, drone_time_matrix)
        else:
            drone_segment_time = 0.0
            drone_path = []

        battery_excess = max(
            0.0,
            drone_segment_time - instance.battery_capacity
        )

        if battery_excess > EPSILON:
            feasible = False
            total_battery_violation += battery_excess

            violations.append({
                "segment": segment_index + 1,
                "from_node": start_node,
                "to_node": end_node,
                "drone_time": float(drone_segment_time),
                "battery_capacity": float(instance.battery_capacity),
                "battery_excess": float(battery_excess)
            })

        if has_drone_flight:
            segment_duration = max(truck_segment_time, drone_segment_time)
        else:
            segment_duration = truck_segment_time

        total_makespan += segment_duration

        segment_details.append({
            "segment": segment_index + 1,
            "from_node": start_node,
            "to_node": end_node,
            "truck_path": truck_path,
            "drone_path": drone_path,
            "truck_time": float(truck_segment_time),
            "drone_time": float(drone_segment_time),
            "segment_duration": float(segment_duration),
            "battery_excess": float(battery_excess)
        })

    alpha = instance.drone_speed / instance.truck_speed

    penalized_objective = (
        total_makespan
        + alpha * total_battery_violation
    )

    return {
        "makespan": float(total_makespan),
        "penalized_objective": float(penalized_objective),
        "feasible": feasible,
        "battery_capacity": float(instance.battery_capacity),
        "total_battery_violation": float(total_battery_violation),
        "alpha": float(alpha),
        "violations": violations,
        "segments": segment_details
    }