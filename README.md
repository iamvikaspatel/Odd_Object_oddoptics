
---

# 🏈 HotStreak Match & Category Data Pipeline

A **modular Python ETL pipeline** designed to extract and merge **match schedules**, **team data**, and **category metadata** from the **HotStreak GraphQL API**.
This project automates fetching upcoming matches, mapping them to their sports and betting categories, and exporting clean, analysis-ready JSON files.

---

## 📁 Project Overview

| Stage                      | Script                | Description                                                      |
| -------------------------- | --------------------- | ---------------------------------------------------------------- |
| **1️⃣ Fetch Match Data**   | `fetch_matches.py`    | Retrieves all scheduled matches with home/away teams and leagues |
| **2️⃣ Fetch Categories**   | `fetch_categories.py` | Extracts sport categories (e.g., *Passing Yards*, *Rushing TDs*) |
| **3️⃣ Combine Data**       | `combine_data.py`     | Merges latest match and category data into unified JSON output   |

---

## ⚙️ Features

* 🏟️ **Match Extraction** — Fetches game schedules, team names, and league data from the HotStreak API
* 🧩 **Category Mapping** — Retrieves every category name, group, and sport association
* 🔄 **Automated Combination** — Joins match and category datasets into a single JSON file
* 🧠 **Error-Resilient Design** — Graceful handling for missing folders, invalid responses, and API timeouts
* 💾 **Versioned Data Output** — Automatically creates timestamped folders for every pipeline run

---

## 🏗️ Project Structure

```
HotStreak-Match-Pipeline/
│
├── src/
│   ├── fetch_matches.py
│   ├── fetch_categories.py
│   ├── combine_data.py
│
├── data/
│   ├── raw/
│   │   ├── matches/
│   │   └── categories/
│   ├── match_object/
│
├── .env
└── README.md
```

---

## 🚀 How It Works

### 1️⃣ Fetch Matches (`fetch_matches.py`)

* Sends a GraphQL request to the HotStreak `/games` API endpoint
* Extracts match ID, home/away team names, start time, and league
* Saves to `data/raw/matches/<timestamp>/matches_raw.json`

Output Example:

```json
[
  {
    "sport_id": "Z2lkOi8vaHMzL1Nwb3J0LzI",
    "id": "Z2lkOi8vaHMzL0dhbWUvOTY4MDU",
    "home_team": "Cle Browns",
    "away_team": "Min Vikings",
    "start_time": "2025-10-05 13:30:00",
    "league": "NFL",
    "odds_count": []
  }
]
```

---

### 2️⃣ Fetch Categories (`fetch_categories.py`)

* Fetches all available **sports and their categories**
* Extracts: sport ID, sport name, category name, and group name
* Saves to `data/raw/categories/<timestamp>/categories_raw.json`

Example Output:

```json
[
  {
    "sport_id": "Z2lkOi8vaHMzL1Nwb3J0LzI",
    "sport_name": "Football",
    "category_id": "Z2lkOi8vaHMzL0NhdGVnb3J5Lzc0",
    "category_name": "Rushing yards",
    "group_name": "offense"
  }
]
```

---

### 3️⃣ Combine Data (`combine_data.py`)

* Reads the latest `matches_raw.json` and `categories_raw.json`
* Maps sport categories to corresponding matches
* Converts `start_time` to human-readable format
* Saves merged output to `data/match_object/matches_with_odds_<timestamp>.json`

Merged Output:

```json
[
  {
    "id": "Z2lkOi8vaHMzL0dhbWUvOTY4MDU",
    "home_team": "Cle Browns",
    "away_team": "Min Vikings",
    "start_time": "2025-10-05 13:30:00",
    "league": "NFL",
    "odds_count": [
      "Rushing yards",
      "Passing TDs",
      "Interceptions thrown"
    ]
  }
]
```

---

## 🧠 Technical Highlights

| Technique                     | Description                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| **GraphQL Queries**           | Fetches deeply nested objects (matches, leagues, and categories) |
| **Dynamic Folder Resolution** | Auto-detects the latest data folders before combining            |
| **Robust Error Handling**     | Recovers gracefully from missing data or invalid JSON            |
| **Time Conversion**           | Converts timestamps → UTC-readable start times                   |

---

## 📦 Installation & Usage

### Prerequisites

* Python **3.9+**
* Dependencies:

  ```bash
  pip install pandas curl_cffi
  ```

### Run Full Sequence

```bash
python fetch_matches.py
python fetch_categories.py
python combine_data.py
```

---

## 📈 Data Flow Summary

```
HotStreak API
   │
   ├──► fetch_matches.py        →  match metadata
   ├──► fetch_categories.py     →  category metadata
   └──► combine_data.py         →  merged match–category dataset
```

---

## 🚀 Future Improvements

* 🧩 **Odds UI Integration** — Extend pipeline to pair each match with its decoded odds and visualize in a dashboard.
* ⚡ **Real-Time Refresh** — Integrate WebSocket updates for live game and odds sync.
* 🕸️ **Asynchronous Fetching** — Parallelize match and category requests for faster scraping.
* 🧠 **Smart Caching** — Cache category data to skip redundant API calls.
* 🧱 **Extended Schema** — Add player or market details once odds data is merged.

---
