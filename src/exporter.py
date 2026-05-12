import pandas as pd
from pathlib import Path


def save_matrix_to_csv(matrix, output_path):
    df = pd.DataFrame(matrix)

    output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f"Saved matrix to: {output_file}")


def save_evaluation_result(result: dict, output_path):
    df = pd.DataFrame([result])

    output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f"Saved evaluation result to: {output_file}")