import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_convergence():
    history_path = Path("results/paper8_ig_sa_history.csv")

    if not history_path.exists():
        raise FileNotFoundError("Run python src/run_paper8_ig_sa.py first.")

    df = pd.read_csv(history_path)

    output_path = Path("results/convergence_plot.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df["iteration"], df["best_cost"])
    plt.xlabel("Iteration")
    plt.ylabel("Best Makespan")
    plt.title("Paper 8 IG-SA Convergence")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved convergence plot to: {output_path}")


def plot_runtime_comparison():
    comparison_path = Path("results/our_baseline_vs_paper_reported.csv")

    if not comparison_path.exists():
        raise FileNotFoundError("Run python src/compare_with_paper.py first.")

    df = pd.read_csv(comparison_path)

    output_path = Path("results/runtime_comparison.png")

    x_labels = df["node_count"].astype(str)

    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, df["ig_sa_runtime_sec"], marker="o", label="Our IG-SA Runtime")
    plt.plot(x_labels, df["paper_ig_avg_time"], marker="o", label="Paper IG Avg Runtime")
    plt.xlabel("Node Count")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison with Paper 8")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved runtime comparison plot to: {output_path}")


def plot_initial_vs_ig_sa():
    benchmark_path = Path("results/baseline_comparison.csv")

    if not benchmark_path.exists():
        raise FileNotFoundError("Run python src/baseline_benchmark.py first.")

    df = pd.read_csv(benchmark_path)

    output_path = Path("results/initial_vs_ig_sa_makespan.png")

    x_labels = df["node_count"].astype(str)

    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, df["initial_makespan"], marker="o", label="Initial Baseline")
    plt.plot(x_labels, df["ig_sa_makespan"], marker="o", label="Paper 8 IG-SA")
    plt.xlabel("Node Count")
    plt.ylabel("Makespan")
    plt.title("Initial Baseline vs Paper 8 IG-SA Makespan")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved makespan comparison plot to: {output_path}")


def plot_multi_run_average_makespan():
    summary_path = Path("results/multi_run_summary.csv")

    if not summary_path.exists():
        raise FileNotFoundError("Run python src/multi_run_benchmark.py first.")

    df = pd.read_csv(summary_path)

    output_path = Path("results/multi_run_average_makespan.png")

    x_labels = df["node_count"].astype(str)

    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, df["average_makespan"], marker="o", label="Average Makespan")
    plt.plot(x_labels, df["best_makespan"], marker="o", label="Best Makespan")
    plt.xlabel("Node Count")
    plt.ylabel("Makespan")
    plt.title("Multi-Run Makespan Results")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved multi-run makespan plot to: {output_path}")


def plot_multi_run_runtime():
    summary_path = Path("results/multi_run_summary.csv")

    if not summary_path.exists():
        raise FileNotFoundError("Run python src/multi_run_benchmark.py first.")

    df = pd.read_csv(summary_path)

    output_path = Path("results/multi_run_runtime.png")

    x_labels = df["node_count"].astype(str)

    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, df["average_runtime_sec"], marker="o", label="Average Runtime")
    plt.xlabel("Node Count")
    plt.ylabel("Runtime (seconds)")
    plt.title("Multi-Run Average Runtime by Node Count")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved multi-run runtime plot to: {output_path}")


if __name__ == "__main__":
    plot_convergence()
    plot_runtime_comparison()
    plot_initial_vs_ig_sa()
    plot_multi_run_average_makespan()
    plot_multi_run_runtime()