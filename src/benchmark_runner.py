from pathlib import Path
import pandas as pd

from data_loader import load_bouman_instance
from models import Solution
from evaluator import evaluate_solution


def run_singlecenter_benchmark(
    data_folder: str = "data/singlecenter",
    output_path: str = "results/singlecenter_benchmark.csv",
    max_files: int = 10
):
    folder = Path(data_folder)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {data_folder}")

    files = sorted([
        file for file in folder.glob("singlecenter-*-n*.txt")
        if "alpha" not in file.name
    ])

    files = files[:max_files]

    results = []

    for file in files:
        print(f"Running: {file.name}")

        instance = load_bouman_instance(str(file))

        node_sequence = list(range(len(instance.nodes)))
        resource_types = [0] + [2] * (len(instance.nodes) - 2) + [0]

        solution = Solution(
            node_sequence=node_sequence,
            resource_types=resource_types
        )

        result = evaluate_solution(instance, solution)

        results.append({
            "instance": instance.name,
            "node_count": len(instance.nodes),
            "truck_speed": instance.truck_speed,
            "drone_speed": instance.drone_speed,
            "battery_capacity": instance.battery_capacity,
            "makespan": result["makespan"],
            "feasible": result["feasible"],
            "violation_count": len(result["violations"])
        })

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

    print(f"Benchmark results saved to: {output_file}")


if __name__ == "__main__":
    run_singlecenter_benchmark()