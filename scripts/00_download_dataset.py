from pathlib import Path

import kagglehub


DATASET_SLUG = "mkechinov/ecommerce-behavior-data-from-multi-category-store"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    dataset_path = Path(kagglehub.dataset_download(DATASET_SLUG))
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    marker_path = RAW_DATA_DIR / "KAGGLE_DATASET_PATH.txt"
    marker_path.write_text(str(dataset_path), encoding="utf-8")

    print("Dataset downloaded by kagglehub.")
    print(f"Dataset cache path: {dataset_path}")
    print(f"Path marker written to: {marker_path}")


if __name__ == "__main__":
    main()
