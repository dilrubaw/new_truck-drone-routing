import time
import pandas as pd
from pathlib import Path

from data_loader import load_bouman_instance
from paper8_ig_sa import paper8_ig_sa
from improved_algorithm import hybrid_ig_sa


def run_solver(solver_name, solver_function, instance):
    start_time = time.time()

    if solver_name == "Paper8 IG-SA":
        best_solution, best_result, history = solver_function(
            instance,
            max_iterations=2000,
            initial_temperature=500.0,
            cooling_rate=0.995,
            time_limit_seconds=60
        )
    else:
        best_solution, best_result, history = solver_function(
            instance,
            max_iterations=2000,
            initial_temperature=500.0,
            base_cooling_rate=0.995,
            stagnation_limit=50,
            time_limit_seconds=60
        )

    runtime = time.time() - start_time

    return best_solution, best_result, history, runtime


def run_multi_run_benchmark(runs_per_instance=5):
    files = [
        "data/singlecenter/singlecenter-1-n5.txt",
        "data/singlecenter/singlecenter-51-n10.txt",
        "data/singlecenter/singlecenter-61-n20.txt",
        "data/singlecenter/singlecenter-71-n50.txt",
    ]

    solvers = [
        ("Paper8 IG-SA", paper8_ig_sa),
        ("Hybrid IG-SA", hybrid_ig_sa),
    ]

    detailed_results = []

    for file_path in files:
        instance = load_bouman_instance(file_path)

        print(f"\nInstance: {instance.name}")

        for solver_name, solver_function in solvers:
            print(f"  Algorithm: {solver_name}")

            for run in range(1, runs_per_instance + 1):
                print(f"    Run {run}/{runs_per_instance}")

                best_solution, best_result, history, runtime = run_solver(
                    solver_name,
                    solver_function,
                    instance
                )

                detailed_results.append({
                    "instance": instance.name,
                    "node_count": len(instance.nodes),
                    "algorithm": solver_name,
                    "run": run,
                    "makespan": best_result["makespan"],
                    "penalized_objective": best_result["penalized_objective"],
                    "feasible": best_result["feasible"],
                    "battery_violation": best_result["total_battery_violation"],
                    "runtime_sec": runtime,
                    "alpha": best_result["alpha"],
                    "battery_capacity": instance.battery_capacity
                })

    detailed_df = pd.DataFrame(detailed_results)

    summary_df = (
        detailed_df
        .groupby(["instance", "node_count", "algorithm"], as_index=False)
        .agg(
            runs=("run", "count"),
            best_makespan=("makespan", "min"),
            worst_makespan=("makespan", "max"),
            average_makespan=("makespan", "mean"),
            std_makespan=("makespan", "std"),
            best_penalized_objective=("penalized_objective", "min"),
            average_penalized_objective=("penalized_objective", "mean"),
            std_penalized_objective=("penalized_objective", "std"),
            average_runtime_sec=("runtime_sec", "mean"),
            best_runtime_sec=("runtime_sec", "min"),
            worst_runtime_sec=("runtime_sec", "max"),
            feasible_runs=("feasible", "sum"),
            average_battery_violation=("battery_violation", "mean"),
            alpha=("alpha", "first"),
            battery_capacity=("battery_capacity", "first")
        )
    )

    comparison_rows = []

    for instance_name in detailed_df["instance"].unique():
        instance_summary = summary_df[summary_df["instance"] == instance_name]

        baseline = instance_summary[
            instance_summary["algorithm"] == "Paper8 IG-SA"
        ]

        hybrid = instance_summary[
            instance_summary["algorithm"] == "Hybrid IG-SA"
        ]

        if baseline.empty or hybrid.empty:
            continue

        baseline_best = float(baseline.iloc[0]["best_makespan"])
        hybrid_best = float(hybrid.iloc[0]["best_makespan"])

        improvement_percent = (
            (baseline_best - hybrid_best) / baseline_best
        ) * 100 if baseline_best != 0 else 0.0

        comparison_rows.append({
            "instance": instance_name,
            "node_count": int(baseline.iloc[0]["node_count"]),
            "baseline_best_makespan": baseline_best,
            "hybrid_best_makespan": hybrid_best,
            "improvement_percent": improvement_percent,
            "baseline_avg_runtime_sec": float(baseline.iloc[0]["average_runtime_sec"]),
            "hybrid_avg_runtime_sec": float(hybrid.iloc[0]["average_runtime_sec"]),
            "baseline_feasible_runs": int(baseline.iloc[0]["feasible_runs"]),
            "hybrid_feasible_runs": int(hybrid.iloc[0]["feasible_runs"])
        })

    comparison_df = pd.DataFrame(comparison_rows)

    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    detailed_path = results_dir / "multi_run_detailed.csv"
    summary_path = results_dir / "multi_run_summary.csv"
    comparison_path = results_dir / "hybrid_vs_baseline_comparison.csv"

    detailed_df.to_csv(detailed_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    comparison_df.to_csv(comparison_path, index=False)

    print(f"\nSaved detailed results to: {detailed_path}")
    print(f"Saved summary results to: {summary_path}")
    print(f"Saved comparison results to: {comparison_path}")


if __name__ == "__main__":
    run_multi_run_benchmark(runs_per_instance=5)