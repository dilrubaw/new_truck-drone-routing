from data_loader import load_bouman_instance
from models import Solution
from evaluator import evaluate_solution

from distance_matrix import (
    compute_distance_matrix,
    compute_truck_time_matrix,
    compute_drone_time_matrix
)

from exporter import (
    save_matrix_to_csv,
    save_evaluation_result
)


def main():
    file_path = "data/singlecenter/singlecenter-61-n20.txt"

    instance = load_bouman_instance(
    file_path=file_path
)

    print("Instance name:", instance.name)
    print("Node count:", len(instance.nodes))
    print("Truck speed:", instance.truck_speed)
    print("Drone speed:", instance.drone_speed)
    print("Battery capacity Q:", instance.battery_capacity)

    # Basit örnek çözüm
    # İlk ve son node synchronization olsun
    node_sequence = list(range(len(instance.nodes)))
    resource_types = [0] + [2] * (len(instance.nodes) - 2) + [0]

    solution = Solution(
        node_sequence=node_sequence,
        resource_types=resource_types
    )

    distance_matrix = compute_distance_matrix(instance)
    truck_matrix = compute_truck_time_matrix(instance)
    drone_matrix = compute_drone_time_matrix(instance)

    save_matrix_to_csv(
        distance_matrix,
        "results/distance_matrix.csv"
    )

    save_matrix_to_csv(
        truck_matrix,
        "results/truck_time_matrix.csv"
    )

    save_matrix_to_csv(
        drone_matrix,
        "results/drone_time_matrix.csv"
    )
    result = evaluate_solution(instance, solution)

    print("Result:")
    print(result)
    save_evaluation_result(
        result,
        "results/evaluation_result.csv"
    )


if __name__ == "__main__":
    main()