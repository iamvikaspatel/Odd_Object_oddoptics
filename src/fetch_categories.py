from curl_cffi import requests
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

API_URL = (
    "https://api3.hotstreak.gg/graphql?"
    "query=query+system+%7B+system+%7B+sports+%7B+id+name+categories+%7B+id+name+groupName+%7D+%7D+%7D+%7D"
)

HEADERS = {
    "origin": "https://hs3.hotstreak.gg",
    "referer": "https://hs3.hotstreak.gg/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "x-hs3-version": "2",
    "x-requested-with": "web",
    "privy-id-token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1TdGIxbUl5M1VPMnd3bDVBSlNiek1sbmd6SWgzRnZfSG9oS0NHV25zSjAifQ.eyJjciI6IjE3NTk1MTcxMTIiLCJsaW5rZWRfYWNjb3VudHMiOiJbe1widHlwZVwiOlwicGhvbmVcIixcInBob25lX251bWJlclwiOlwiKzEgMjQwIDM1MSA1NzIwXCIsXCJsdlwiOjE3NTk1Mzk4NTZ9LHtcInR5cGVcIjpcIndhbGxldFwiLFwiYWRkcmVzc1wiOlwiQXhtTUZQYW90ZTFYYlRnc2tDcURuMnc0SmlFSkN5SnZIb3Q0enlzSmVCWEJcIixcImNoYWluX3R5cGVcIjpcInNvbGFuYVwiLFwid2FsbGV0X2NsaWVudF90eXBlXCI6XCJwcml2eVwiLFwibHZcIjoxNzU5NTE3MTEzfV0iLCJpc3MiOiJwcml2eS5pbyIsImlhdCI6MTc1OTcwMzQxNiwiYXVkIjoiY205YWdyZWR5MDFjNWpsMG16dnhibW42NSIsInN1YiI6ImRpZDpwcml2eTpjbWdiNzI0dzcwMHRlbDQwY3NlOGFpNGIzIiwiZXhwIjoxNzU5NzA3MDE2fQ.quPLreW_p7g7S2AasV4cbXtaMThNawwyJRc4UIs1AfJimKCkVHWsp1T-oWfUHXRlxRQyV2wB1Cs9emiw5yInog"  # 🔐 Replace with your valid token
}

def fetch_categories():
    """Fetch categories safely and save to timestamped folder."""
    try:
        response = requests.get(API_URL, headers=HEADERS, impersonate="chrome", timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.RequestsError as e:
        print(f"❌ Network error fetching categories: {e}")
        return pd.DataFrame()
    except ValueError:
        print("❌ Invalid JSON in categories response.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return pd.DataFrame()

    sports = data.get("data", {}).get("system", {}).get("sports")
    if not sports:
        print("⚠️ No sports data found in response.")
        return pd.DataFrame()

    rows = []
    for sport in sports:
        sport_id = sport.get("id")
        sport_name = sport.get("name")
        for cat in sport.get("categories", []):
            rows.append({
                "sport_id": sport_id,
                "sport_name": sport_name,
                "category_id": cat.get("id"),
                "category_name": cat.get("name"),
                "group_name": cat.get("groupName")
            })

    df = pd.DataFrame(rows)

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = Path(f"data/raw/categories/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "categories_raw.json"
        df.to_json(output_path, orient='records', indent=2)
        print(f"✅ {len(df)} categories saved to {output_path}")
    except Exception as e:
        print(f"❌ Failed to save categories JSON: {e}")

    return df


if __name__ == "__main__":
    fetch_categories()
