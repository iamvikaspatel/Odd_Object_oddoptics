from curl_cffi import requests
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import pandas as pd
from pathlib import Path

# =============================
# 🔹 Configuration
# =============================

API_URL = "https://api3.hotstreak.gg/graphql"

HEADERS = {
    "origin": "https://hs3.hotstreak.gg",
    "referer": "https://hs3.hotstreak.gg/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "x-hs3-version": "2",
    "x-requested-with": "web",
    "privy-id-token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1TdGIxbUl5M1VPMnd3bDVBSlNiek1sbmd6SWgzRnZfSG9oS0NHV25zSjAifQ.eyJjciI6IjE3NTk1MTcxMTIiLCJsaW5rZWRfYWNjb3VudHMiOiJbe1widHlwZVwiOlwicGhvbmVcIixcInBob25lX251bWJlclwiOlwiKzEgMjQwIDM1MSA1NzIwXCIsXCJsdlwiOjE3NTk1Mzk4NTZ9LHtcInR5cGVcIjpcIndhbGxldFwiLFwiYWRkcmVzc1wiOlwiQXhtTUZQYW90ZTFYYlRnc2tDcURuMnc0SmlFSkN5SnZIb3Q0enlzSmVCWEJcIixcImNoYWluX3R5cGVcIjpcInNvbGFuYVwiLFwid2FsbGV0X2NsaWVudF90eXBlXCI6XCJwcml2eVwiLFwibHZcIjoxNzU5NTE3MTEzfV0iLCJpc3MiOiJwcml2eS5pbyIsImlhdCI6MTc1OTcwMzQxNiwiYXVkIjoiY205YWdyZWR5MDFjNWpsMG16dnhibW42NSIsInN1YiI6ImRpZDpwcml2eTpjbWdiNzI0dzcwMHRlbDQwY3NlOGFpNGIzIiwiZXhwIjoxNzU5NzA3MDE2fQ.quPLreW_p7g7S2AasV4cbXtaMThNawwyJRc4UIs1AfJimKCkVHWsp1T-oWfUHXRlxRQyV2wB1Cs9emiw5yInog"  # 🔐 Replace with your valid token
}

query_games = """
query games {
  games {
    id
    opponents { designation team { abbreviation name } }
    league { name sportId }
    scheduledAt
  }
}
"""

@dataclass
class Match:
    id: str
    home_team: str
    away_team: str
    start_time: datetime
    league: str
    sport_id: str
    odds: List = field(default_factory=list)


def fetch_matches():
    """Fetch matches safely and save to timestamped folder."""
    payload = {"query": query_games, "operationName": "games"}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, impersonate="chrome", timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.RequestsError as e:
        print(f"❌ Network error fetching matches: {e}")
        return pd.DataFrame()
    except ValueError:
        print("❌ Invalid JSON in API response.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return pd.DataFrame()

    games = data.get("data", {}).get("games")
    if not games:
        print("⚠️ No game data found in API response.")
        return pd.DataFrame()

    rows = []
    for g in games:
        home_team, away_team = "Unknown", "Unknown"
        for opp in g.get("opponents", []):
            team = opp.get("team", {})
            name = f"{team.get('abbreviation', '').strip()} {team.get('name', '').strip()}".strip()
            if opp.get("designation") == "home":
                home_team = name
            elif opp.get("designation") == "away":
                away_team = name

        rows.append({
            "sport_id": g.get("league", {}).get("sportId", "Unknown"),
            "id": g.get("id"),
            "home_team": home_team,
            "away_team": away_team,
            "start_time": g.get("scheduledAt"),
            "league": g.get("league", {}).get("name", "Unknown"),
            "odds_count": []
        })

    df = pd.DataFrame(rows)

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = Path(f"data/raw/matches/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "matches_raw.json"
        df.to_json(output_path, orient='records', indent=2)
        print(f"✅ {len(df)} matches saved to {output_path}")
    except Exception as e:
        print(f"❌ Failed to save matches JSON: {e}")

    return df


if __name__ == "__main__":
    fetch_matches()
