import pandas as pd
from pathlib import Path


def save_paper_reported_results():
    data = [
        {"scenario": "1-center", "alpha": 1, "node_count": 5, "paper_ig_avg_rpd": 0.5, "paper_ig_avg_time": 0.1},
        {"scenario": "1-center", "alpha": 1, "node_count": 10, "paper_ig_avg_rpd": 1.3, "paper_ig_avg_time": 0.6},
        {"scenario": "1-center", "alpha": 1, "node_count": 20, "paper_ig_avg_rpd": 4.4, "paper_ig_avg_time": 3.6},
        {"scenario": "1-center", "alpha": 1, "node_count": 50, "paper_ig_avg_rpd": 0.8, "paper_ig_avg_time": 49.1},

        {"scenario": "1-center", "alpha": 2, "node_count": 5, "paper_ig_avg_rpd": 0.0, "paper_ig_avg_time": 0.1},
        {"scenario": "1-center", "alpha": 2, "node_count": 10, "paper_ig_avg_rpd": 1.4, "paper_ig_avg_time": 0.7},
        {"scenario": "1-center", "alpha": 2, "node_count": 20, "paper_ig_avg_rpd": 0.0, "paper_ig_avg_time": 3.6},
        {"scenario": "1-center", "alpha": 2, "node_count": 50, "paper_ig_avg_rpd": 0.6, "paper_ig_avg_time": 50.4},

        {"scenario": "1-center", "alpha": 3, "node_count": 5, "paper_ig_avg_rpd": 0.0, "paper_ig_avg_time": 0.1},
        {"scenario": "1-center", "alpha": 3, "node_count": 10, "paper_ig_avg_rpd": 1.9, "paper_ig_avg_time": 0.7},
        {"scenario": "1-center", "alpha": 3, "node_count": 20, "paper_ig_avg_rpd": 0.0, "paper_ig_avg_time": 3.5},
        {"scenario": "1-center", "alpha": 3, "node_count": 50, "paper_ig_avg_rpd": 0.7, "paper_ig_avg_time": 50.7},
    ]

    output_path = Path("results/paper_reported_1center_results.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

    print(f"Saved paper reported results to: {output_path}")
    print(df)


if __name__ == "__main__":
    save_paper_reported_results()