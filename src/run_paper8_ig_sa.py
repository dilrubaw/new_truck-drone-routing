import pandas as pd
from pathlib import Path

from data_loader import load_bouman_instance
from paper8_ig_sa import paper8_ig_sa
from exporter import save_evaluation_result


def save_history(history, output_path):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(history)
    df.to_csv(output_file, index=False)

    print(f"Saved convergence history to: {output_file}")


def main():
    file_path = "data/singlecenter/singlecenter-61-n20.txt"

    instance = load_bouman_instance(file_path)

    best_solution, best_result, history = paper8_ig_sa(
        instance,
        max_iterations=2000,
        initial_temperature=500.0,
        cooling_rate=0.995,
        time_limit_seconds=60
    )

    print("Instance:", instance.name)
    print("Node count:", len(instance.nodes))
    print("Best node sequence:")
    print(best_solution.node_sequence)
    print("Best resource types:")
    print(best_solution.resource_types)
    print("Best result:")
    print(best_result)

    save_evaluation_result(
        best_result,
        "results/paper8_ig_sa_result.csv"
    )

    save_history(
        history,
        "results/paper8_ig_sa_history.csv"
    )


if __name__ == "__main__":
    main()