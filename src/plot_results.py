from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_makespan_comparison(df, output_dir):
    pivot = df.set_index("instance")

    plt.figure(figsize=(10, 6))

    x = range(len(pivot))

    plt.bar(
        [i - 0.2 for i in x],
        pivot["baseline_best_makespan"],
        width=0.4,
        label="Paper8 IG-SA"
    )

    plt.bar(
        [i + 0.2 for i in x],
        pivot["hybrid_best_makespan"],
        width=0.4,
        label="Hybrid IG-SA"
    )

    plt.xticks(list(x), pivot.index, rotation=15)

    plt.ylabel("Best Makespan")
    plt.title("Baseline vs Hybrid Makespan Comparison")
    plt.legend()

    plt.tight_layout()

    path = output_dir / "hybrid_vs_baseline_makespan.png"

    plt.savefig(path)

    print(f"Saved: {path}")


def plot_runtime_comparison(df, output_dir):
    pivot = df.set_index("instance")

    plt.figure(figsize=(10, 6))

    x = range(len(pivot))

    plt.bar(
        [i - 0.2 for i in x],
        pivot["baseline_avg_runtime_sec"],
        width=0.4,
        label="Paper8 IG-SA"
    )

    plt.bar(
        [i + 0.2 for i in x],
        pivot["hybrid_avg_runtime_sec"],
        width=0.4,
        label="Hybrid IG-SA"
    )

    plt.xticks(list(x), pivot.index, rotation=15)

    plt.ylabel("Average Runtime (sec)")
    plt.title("Baseline vs Hybrid Runtime Comparison")
    plt.legend()

    plt.tight_layout()

    path = output_dir / "hybrid_vs_baseline_runtime.png"

    plt.savefig(path)

    print(f"Saved: {path}")


def plot_improvement(df, output_dir):
    plt.figure(figsize=(10, 6))

    plt.bar(
        df["instance"],
        df["improvement_percent"]
    )

    plt.ylabel("Improvement (%)")
    plt.title("Hybrid Improvement Over Baseline")

    plt.xticks(rotation=15)

    plt.tight_layout()

    path = output_dir / "hybrid_improvement_percent.png"

    plt.savefig(path)

    print(f"Saved: {path}")


if __name__ == "__main__":
    results_path = Path("results/hybrid_vs_baseline_comparison.csv")

    df = pd.read_csv(results_path)

    output_dir = Path("results")

    plot_makespan_comparison(df, output_dir)
    plot_runtime_comparison(df, output_dir)
    plot_improvement(df, output_dir)