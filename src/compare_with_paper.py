import pandas as pd
from pathlib import Path


def compare_with_paper():
    our_results_path = Path("results/baseline_comparison.csv")
    paper_results_path = Path("results/paper_reported_1center_results.csv")

    if not our_results_path.exists():
        raise FileNotFoundError("Run python src/baseline_benchmark.py first.")

    if not paper_results_path.exists():
        raise FileNotFoundError("Run python src/paper_reported_results.py first.")

    our_df = pd.read_csv(our_results_path)
    paper_df = pd.read_csv(paper_results_path)

    # Şu an sizin dataset dosyalarınız alpha etiketsiz olduğu için default alpha=1 kabul ediyoruz.
    our_df["alpha"] = 1

    comparison = our_df.merge(
        paper_df,
        on=["node_count", "alpha"],
        how="left"
    )

    comparison["runtime_ratio_our_vs_paper"] = (
        comparison["ig_sa_runtime_sec"] / comparison["paper_ig_avg_time"]
    )

    output_path = Path("results/our_baseline_vs_paper_reported.csv")
    comparison.to_csv(output_path, index=False)

    print(f"Saved comparison to: {output_path}")
    print(comparison)


if __name__ == "__main__":
    compare_with_paper()