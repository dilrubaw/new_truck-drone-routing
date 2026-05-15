import time
import pandas as pd
from pathlib import Path

from data_loader import load_bouman_instance
from initial_solution import create_initial_solution
from paper8_ig_sa import paper8_ig_sa
from evaluator import evaluate_solution


def run_multi_run_benchmark(runs_per_instance=5):
    files = [
        "data/singlecenter/singlecenter-1-n5.txt",
        "data/singlecenter/singlecenter-51-n10.txt",
        "data/singlecenter/singlecenter-61-n20.txt",
        "data/singlecenter/singlecenter-71-n50.txt",
    ]

    summary_results = []
    detailed_results = []

    for file_path in files:
        instance = load_bouman_instance(file_path)

        print(f"\nInstance: {instance.name}")

        run_makespans = []
        run_runtimes = []

        for run in range(1, runs_per_instance + 1):
            print(f"  Run {run}/{runs_per_instance}")

            start_time = time.time()

            best_solution, best_result, history = paper8_ig_sa(
                instance,
                max_iterations=2000,
                initial_temperature=500.0,
                cooling_rate=0.995,
                time_limit_seconds=60
            )

            runtime = time.time() - start_time

            run_makespans.append(best_result["makespan"])
            run_objectives = []
            run_runtimes.append(runtime)
            run_objectives.append(best_result["penalized_objective"])

            detailed_results.append({
                "instance": instance.name,
                "node_count": len(instance.nodes),
                "run": run,

                "makespan": best_result["makespan"],
                "penalized_objective": best_result["penalized_objective"],

                "feasible": best_result["feasible"],

                "battery_violation": best_result["total_battery_violation"],

                "runtime_sec": runtime,

                "alpha": best_result["alpha"],

                "battery_capacity": instance.battery_capacity
            })

        summary_results.append({
            "instance": instance.name,
            "node_count": len(instance.nodes),
            "runs": runs_per_instance,

            "best_makespan": min(run_makespans),
            "worst_makespan": max(run_makespans),
            "average_makespan": sum(run_makespans) / len(run_makespans),

            "std_makespan": pd.Series(run_makespans).std(),

            "average_runtime_sec": sum(run_runtimes) / len(run_runtimes),
            "best_runtime_sec": min(run_runtimes),
            "worst_runtime_sec": max(run_runtimes),

            "alpha": instance.drone_speed / instance.truck_speed,

            "battery_capacity": instance.battery_capacity,
            "best_penalized_objective": min(run_objectives),
            "average_penalized_objective": sum(run_objectives) / len(run_objectives),
            "std_penalized_objective": pd.Series(run_objectives).std()
        })
    summary_path = Path("results/multi_run_summary.csv")
    detailed_path = Path("results/multi_run_detailed.csv")

    summary_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(summary_results).to_csv(summary_path, index=False)
    pd.DataFrame(detailed_results).to_csv(detailed_path, index=False)

    print(f"\nSaved summary results to: {summary_path}")
    print(f"Saved detailed results to: {detailed_path}")


if __name__ == "__main__":
    run_multi_run_benchmark(runs_per_instance=5)