import csv
import time
from pathlib import Path

from data_loader import load_bouman_instance
from paper8_ig_sa import paper8_ig_sa
from improved_algorithm import hybrid_ig_sa


INSTANCE_BY_NODE_COUNT = {
    5: "data/singlecenter/singlecenter-1-n5.txt",
    10: "data/singlecenter/singlecenter-51-n10.txt",
    20: "data/singlecenter/singlecenter-61-n20.txt",
    50: "data/singlecenter/singlecenter-71-n50.txt",
}


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        return

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def run_benchmark():
    detailed_rows = []
    summary_rows = []
    comparison_rows = []

    for node_count, instance_path in INSTANCE_BY_NODE_COUNT.items():
        instance = load_bouman_instance(Path(instance_path))

        print(f"\nRunning n={node_count}")

        baseline_start = time.time()
        _, baseline_result, _ = paper8_ig_sa(
            instance,
            max_iterations=300,
            initial_temperature=500.0,
            cooling_rate=0.995,
            time_limit_seconds=8
        )
        baseline_runtime = time.time() - baseline_start

        hybrid_start = time.time()
        _, hybrid_result, _ = hybrid_ig_sa(
            instance,
            max_iterations=300,
            initial_temperature=500.0,
            base_cooling_rate=0.995,
            stagnation_limit=50,
            time_limit_seconds=8
        )
        hybrid_runtime = time.time() - hybrid_start

        baseline = baseline_result["makespan"]
        hybrid = hybrid_result["makespan"]

        improvement = ((baseline - hybrid) / baseline) * 100 if baseline else 0.0

        row = {
            "instance": instance.name,
            "nodes": node_count,
            "baseline_makespan": baseline,
            "hybrid_makespan": hybrid,
            "improvement_percent": improvement,
            "baseline_runtime": baseline_runtime,
            "hybrid_runtime": hybrid_runtime,
            "baseline_feasible": baseline_result["feasible"],
            "hybrid_feasible": hybrid_result["feasible"],
            "baseline_battery_violation": baseline_result["total_battery_violation"],
            "hybrid_battery_violation": hybrid_result["total_battery_violation"],
        }

        print(
            f"Baseline={baseline:.4f}, "
            f"Hybrid={hybrid:.4f}, "
            f"Improvement={improvement:.2f}%"
        )

        detailed_rows.append(row)

        summary_rows.append({
            "instance": instance.name,
            "nodes": node_count,
            "avg_baseline_makespan": baseline,
            "avg_hybrid_makespan": hybrid,
            "avg_improvement_percent": improvement,
            "avg_baseline_runtime": baseline_runtime,
            "avg_hybrid_runtime": hybrid_runtime,
        })

        comparison_rows.append({
            "instance": instance.name,
            "baseline_makespan": baseline,
            "hybrid_makespan": hybrid,
            "improvement_percent": improvement,
        })

        write_csv("results/multi_run_detailed.csv", detailed_rows)
        write_csv("results/multi_run_summary.csv", summary_rows)
        write_csv("results/hybrid_vs_baseline_comparison.csv", comparison_rows)

    print("\nBenchmark completed.")


if __name__ == "__main__":
    run_benchmark()