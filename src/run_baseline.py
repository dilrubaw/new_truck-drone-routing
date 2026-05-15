from data_loader import load_bouman_instance
from initial_solution import create_initial_solution
from evaluator import evaluate_solution
from exporter import save_evaluation_result


def main():
    file_path = "data/singlecenter/singlecenter-61-n20.txt"

    instance = load_bouman_instance(file_path)

    solution = create_initial_solution(instance)

    result = evaluate_solution(instance, solution)

    print("Instance:", instance.name)
    print("Node count:", len(instance.nodes))
    print("Node sequence:")
    print(solution.node_sequence)
    print("Resource types:")
    print(solution.resource_types)
    print("Result:")
    print(result)

    save_evaluation_result(
        result,
        "results/paper8_baseline_result.csv"
    )


if __name__ == "__main__":
    main()