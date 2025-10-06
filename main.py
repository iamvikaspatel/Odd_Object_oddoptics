import sys
from pathlib import Path
import traceback

# Add src folder to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from fetch_matches import fetch_matches
from fetch_categories import fetch_categories
from combine_data import combine_data


def run_step(step_name, func):
    """Run a pipeline step safely with error handling and clean logs."""
    print(f"\n{'=' * 80}\n🧩 {step_name}\n{'=' * 80}")
    try:
        func()
        print(f"✅ {step_name} completed successfully.")
    except Exception as e:
        print(f"❌ Error in {step_name}: {e}")
        traceback.print_exc()
        sys.exit(1)  # Stop pipeline safely


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🧩 🔥 Starting HotStreak Data Pipeline 🔥")
    print("=" * 80)

    try:
        run_step("STEP 1️⃣ - Fetching Odds Data", fetch_matches)
        run_step("STEP 2️⃣ - Fetching Category Name Data", fetch_categories)
        run_step("STEP 3️⃣ - Merging Odds and Category Names", combine_data)
    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrupted manually. Exiting safely...")
        sys.exit(0)

    print("\n" + "=" * 80)
    print("🏁 ✅ All steps completed successfully.")
    print("=" * 80)
