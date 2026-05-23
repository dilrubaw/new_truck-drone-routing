import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


RESULTS_DIR = Path("results")


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    summary_path = RESULTS_DIR / "multi_run_summary.csv"

    if not summary_path.exists():
        raise FileNotFoundError("results/multi_run_summary.csv not found. Run experiment_runner.py first.")

    summary = pd.read_csv(summary_path)

    nodes = summary["nodes"]

    plt.figure(figsize=(8, 5))
    plt.plot(nodes, summary["avg_baseline_makespan"], marker="o", label="Baseline")
    plt.plot(nodes, summary["avg_hybrid_makespan"], marker="o", label="Hybrid")
    plt.xlabel("Node Count")
    plt.ylabel("Makespan")
    plt.title("Hybrid vs Baseline Makespan")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "hybrid_vs_baseline_makespan.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(nodes, summary["avg_improvement_percent"], marker="o")
    plt.xlabel("Node Count")
    plt.ylabel("Improvement (%)")
    plt.title("Hybrid Improvement Percentage")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "hybrid_improvement_percent.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(nodes, summary["avg_baseline_runtime"], marker="o", label="Baseline")
    plt.plot(nodes, summary["avg_hybrid_runtime"], marker="o", label="Hybrid")
    plt.xlabel("Node Count")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "hybrid_vs_baseline_runtime.png", dpi=200)
    plt.close()

    print("Generated:")
    print(RESULTS_DIR / "hybrid_vs_baseline_makespan.png")
    print(RESULTS_DIR / "hybrid_improvement_percent.png")
    print(RESULTS_DIR / "hybrid_vs_baseline_runtime.png")


if __name__ == "__main__":
    main()