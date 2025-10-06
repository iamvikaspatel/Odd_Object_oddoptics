import pandas as pd
from pathlib import Path
from datetime import datetime

def get_latest_subdir(path: Path):
    """Return latest subdirectory by modification time."""
    try:
        subdirs = [d for d in path.iterdir() if d.is_dir()]
        if not subdirs:
            return None
        return max(subdirs, key=lambda d: d.stat().st_mtime)
    except Exception as e:
        print(f"❌ Error scanning folders: {e}")
        return None


def combine_data():
    """Safely combine latest matches and categories JSON files."""
    matches_root = Path("data/raw/matches")
    categories_root = Path("data/raw/categories")

    latest_matches = get_latest_subdir(matches_root)
    latest_categories = get_latest_subdir(categories_root)

    if not latest_matches or not latest_categories:
        print("❌ Missing data folders — run fetch scripts first.")
        return

    matches_file = latest_matches / "matches_raw.json"
    categories_file = latest_categories / "categories_raw.json"

    if not matches_file.exists() or not categories_file.exists():
        print("❌ Missing one or both JSON files. Please check raw folders.")
        return

    try:
        df_matches = pd.read_json(matches_file)
        df_categories = pd.read_json(categories_file)
    except Exception as e:
        print(f"❌ Error reading JSON files: {e}")
        return

    if df_matches.empty or df_categories.empty:
        print("⚠️ One of the datasets is empty. Skipping merge.")
        return

    # Convert start_time from timestamp to human-readable format
    try:
        if 'start_time' in df_matches.columns:
            df_matches['start_time'] = pd.to_datetime(df_matches['start_time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"⚠️ Warning: Could not convert start_time format: {e}")

    try:
        sport_categories = (
            df_categories.groupby("sport_id")["category_name"]
            .apply(list)
            .to_dict()
        )
        df_matches["odds_count"] = df_matches["sport_id"].map(sport_categories)
        df_matches["odds_count"] = df_matches["odds_count"].apply(
            lambda x: x if isinstance(x, list) else []
        )
        # Remove sport_id from final output
        df_matches = df_matches.drop(columns=['sport_id'], errors='ignore')
    except Exception as e:
        print(f"❌ Error combining data: {e}")
        return

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"matches_with_odds_{timestamp}.json"
        df_matches.to_json(output_path, orient='records', indent=2)
        print(f"✅ Combined file saved successfully → {output_path}")
    except Exception as e:
        print(f"❌ Failed to save combined JSON: {e}")

    return df_matches


if __name__ == "__main__":
    combine_data()
