from models import ProblemInstance, Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def path_time(path, time_matrix):
    total = 0.0

    for i in range(len(path) - 1):
        total += time_matrix[path[i]][path[i + 1]]

    return total


def validate_solution(solution: Solution):
    seq = solution.node_sequence
    types = solution.resource_types

    if len(seq) != len(types):
        raise ValueError("pi_s and pi_t must have the same length.")

    if len(seq) < 2:
        raise ValueError("Solution must contain at least origin and end node.")

    if types[0] != 0 or types[-1] != 0:
        raise ValueError("First and last nodes must be synchronization nodes with type 0.")

    for resource_type in types:
        if resource_type not in [0, 1, 2]:
            raise ValueError("Resource types must be 0, 1, or 2.")


def evaluate_solution(instance: ProblemInstance, solution: Solution) -> dict:
    """
    Evaluates a truck-drone solution.

    pi_s = node_sequence
    pi_t = resource_types

    Resource types:
    0 = truck + drone synchronization node
    1 = drone only
    2 = truck only

    Paper 8 penalized objective:
    f = s_e + p * max(0, q_r - Q)

    p = alpha = drone_speed / truck_speed
    """

    validate_solution(solution)

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

        battery_excess = max(
            0.0,
            drone_segment_time - instance.battery_capacity
        )

        if battery_excess > 0:
            feasible = False
            total_battery_violation += battery_excess

            violations.append({
                "segment": segment_index + 1,
                "from_node": segment_nodes[0],
                "to_node": segment_nodes[-1],
                "drone_time": float(drone_segment_time),
                "battery_capacity": float(instance.battery_capacity),
                "battery_excess": float(battery_excess)
            })

        total_makespan += max(truck_segment_time, drone_segment_time)

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
        "violations": violations
    }