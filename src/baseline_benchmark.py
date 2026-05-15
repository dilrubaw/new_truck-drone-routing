import time
import pandas as pd
from pathlib import Path

from data_loader import load_bouman_instance
from initial_solution import create_initial_solution
from paper8_ig_sa import paper8_ig_sa
from evaluator import evaluate_solution


def run_baseline_benchmark():
    files = [
        "data/singlecenter/singlecenter-1-n5.txt",
        "data/singlecenter/singlecenter-51-n10.txt",
        "data/singlecenter/singlecenter-61-n20.txt",
        "data/singlecenter/singlecenter-71-n50.txt",
    ]

    results = []

    for file_path in files:
        print(f"Running benchmark for: {file_path}")

        instance = load_bouman_instance(file_path)

        start = time.time()
        initial_solution = create_initial_solution(instance)
        initial_result = evaluate_solution(instance, initial_solution)
        initial_runtime = time.time() - start

        start = time.time()
        ig_solution, ig_result, history = paper8_ig_sa(
            instance,
            max_iterations=2000,
            initial_temperature=500.0,
            cooling_rate=0.995,
            time_limit_seconds=60
        )
        ig_runtime = time.time() - start

        improvement = (
            (initial_result["makespan"] - ig_result["makespan"])
            / initial_result["makespan"]
        ) * 100

        results.append({
            "instance": instance.name,
            "node_count": len(instance.nodes),
            "initial_makespan": initial_result["makespan"],
            "ig_sa_makespan": ig_result["makespan"],
            "improvement_percent": improvement,
            "initial_feasible": initial_result["feasible"],
            "ig_sa_feasible": ig_result["feasible"],
            "initial_runtime_sec": initial_runtime,
            "ig_sa_runtime_sec": ig_runtime,
            "battery_capacity": instance.battery_capacity
        })

    output_path = Path("results/baseline_comparison.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)

    print(f"Saved baseline comparison to: {output_path}")
    print(df)


if __name__ == "__main__":
    run_baseline_benchmark()