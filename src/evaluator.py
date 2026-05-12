from models import ProblemInstance, Solution
from distance_matrix import compute_truck_time_matrix, compute_drone_time_matrix


def evaluate_solution(instance: ProblemInstance, solution: Solution) -> dict:
    """
    Solution için:
    - makespan hesaplar
    - battery feasibility kontrol eder
    """

    truck_time_matrix = compute_truck_time_matrix(instance)
    drone_time_matrix = compute_drone_time_matrix(instance)

    seq = solution.node_sequence
    types = solution.resource_types

    if len(seq) != len(types):
        raise ValueError("node_sequence and resource_types must have same length.")

    truck_time = 0.0
    drone_time = 0.0
    total_makespan = 0.0

    current_drone_battery_usage = 0.0
    feasible = True
    violations = []

    for i in range(len(seq) - 1):
        current_node = seq[i]
        next_node = seq[i + 1]

        current_type = types[i]
        next_type = types[i + 1]

        edge_truck_time = truck_time_matrix[current_node][next_node]
        edge_drone_time = drone_time_matrix[current_node][next_node]

        # Eğer sonraki node truck veya both ise truck gider
        if next_type in [0, 2]:
            truck_time += edge_truck_time

        # Eğer sonraki node drone veya both ise drone gider
        if next_type in [0, 1]:
            drone_time += edge_drone_time
            current_drone_battery_usage += edge_drone_time

        # Synchronization node: type 0
        if next_type == 0:
            segment_time = max(truck_time, drone_time)
            total_makespan += segment_time

            if current_drone_battery_usage > instance.battery_capacity:
                feasible = False
                violations.append({
                    "at_node": next_node,
                    "battery_used": current_drone_battery_usage,
                    "battery_capacity": instance.battery_capacity
                })

            truck_time = 0.0
            drone_time = 0.0
            current_drone_battery_usage = 0.0

    return {
    "makespan": float(total_makespan),
    "feasible": feasible,
    "battery_capacity": float(instance.battery_capacity),
    "violations": violations
}