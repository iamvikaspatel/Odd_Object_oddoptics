# 🎯 OpticOdds - HotStreak Data Pipeline

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust, modular Python ETL pipeline that fetches **match** and **category** data from the HotStreak GraphQL API, bypasses Cloudflare protection, and produces timestamped JSON outputs ready for analysis.

## � Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Module Overview](#-module-overview)
- [Output Format](#-output-format)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🔐 **Cloudflare Bypass**: Uses `curl_cffi` to seamlessly bypass Cloudflare protection
- 🛡️ **Robust Error Handling**: Gracefully handles API failures, missing data, and network issues
- 📁 **Timestamped Outputs**: Automatic versioning with timestamps for all raw and processed data
- 🔄 **Modular Architecture**: Separate modules for fetching, processing, and combining data
- 📊 **Production-Ready**: Clean code structure, comprehensive error handling, and logging
- 🐍 **Python 3.9+**: Compatible with modern Python versions
- 🚀 **Easy to Use**: Single command execution with `main.py`

---

## 📂 Project Structure

```
opticOdds/
├── data/
│   ├── raw/
│   │   ├── matches/
│   │   │   └── YYYY-MM-DD_HH-MM-SS/
│   │   │       └── matches_raw.json
│   │   └── categories/
│   │       └── YYYY-MM-DD_HH-MM-SS/
│   │           └── categories_raw.json
│   └── processed/
│       └── matches_with_odds_YYYY-MM-DD_HH-MM-SS.json
├── src/
│   ├── fetch_matches.py      # Fetches game/match data from API
│   ├── fetch_categories.py   # Fetches sports categories and odds types
│   └── combine_data.py        # Merges matches with category data
├── main.py                    # Main orchestrator script
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

---

## 🔧 Prerequisites

- **Python**: 3.9 or higher
- **pip**: Latest version recommended
- **Git**: For cloning the repository
- **HotStreak Account**: Valid authentication token required

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone git@github.com:iamvikaspatel/opticOdds.git
cd opticOdds
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies:**

- `curl_cffi` - For bypassing Cloudflare protection
- `pandas` - Data manipulation and JSON handling
- `requests` - HTTP library (fallback)
- `python-dateutil` - Date parsing utilities
- `pytz` - Timezone handling

---

## ⚙️ Configuration

### Obtain Authentication Token

1. Open [HotStreak](https://hs3.hotstreak.gg/) in your browser
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to the **Network** tab
4. Refresh the page or perform an action
5. Look for GraphQL requests to `api3.hotstreak.gg`
6. Click on the request and go to **Headers**
7. Copy the value of `privy-id-token`

### Update Token in Scripts

Edit the following files and replace the token:

**`src/fetch_matches.py`** (around line 20):

```python
HEADERS = {
    # ... other headers ...
    "privy-id-token": "YOUR_ACTUAL_TOKEN_HERE"
}
```

**`src/fetch_categories.py`** (around line 17):

```python
HEADERS = {
    # ... other headers ...
    "privy-id-token": "YOUR_ACTUAL_TOKEN_HERE"
}
```

> ⚠️ **Security Note**: Never commit your actual token to version control. Consider using environment variables for production deployments.

---

## 🚀 Usage

### Quick Start (All Steps)

Run the entire pipeline with a single command:

```bash
python main.py
```

This will:

1. Fetch all upcoming matches
2. Fetch sports categories and odds types
3. Combine both datasets
4. Save timestamped outputs

### Individual Modules

You can also run each module independently:

#### Fetch Matches Only

```bash
python src/fetch_matches.py
```

**Output**: `data/raw/matches/YYYY-MM-DD_HH-MM-SS/matches_raw.json`

#### Fetch Categories Only

```bash
python src/fetch_categories.py
```

**Output**: `data/raw/categories/YYYY-MM-DD_HH-MM-SS/categories_raw.json`

#### Combine Data Only

```bash
python src/combine_data.py
```

**Output**: `data/processed/matches_with_odds_YYYY-MM-DD_HH-MM-SS.json`

> 📝 **Note**: `combine_data.py` automatically uses the latest timestamped data from both sources.

---

## 🧩 Module Overview

### 📄 `fetch_matches.py`

**Purpose**: Fetches upcoming game/match data from HotStreak GraphQL API.

**Key Features**:

- Queries game schedules with team information
- Extracts match IDs, home/away teams, league, sport ID, and start times
- Saves to timestamped JSON in `data/raw/matches/`

**Output Columns**:

- `id` - Unique match identifier
- `home_team` - Home team name
- `away_team` - Away team name
- `start_time` - Scheduled match start time (ISO 8601)
- `league` - League/competition name
- `sport_id` - Sport identifier
- `odds` - List of available odds (initially empty)

---

### 📄 `fetch_categories.py`

**Purpose**: Fetches sports categories and available betting types.

**Key Features**:

- Retrieves all sports and their associated categories
- Extracts sport IDs, names, category types, and group names
- Saves to timestamped JSON in `data/raw/categories/`

**Output Columns**:

- `sport_id` - Sport identifier
- `sport_name` - Sport name (e.g., "Basketball", "Soccer")
- `category_id` - Category/odds type ID
- `category_name` - Category name (e.g., "Moneyline", "Spread")
- `group_name` - Category group classification

---

### 📄 `combine_data.py`

**Purpose**: Merges match data with available odds categories.

**Key Features**:

- Automatically locates latest match and category data
- Joins data based on `sport_id`
- Enriches matches with available odds types for their sport
- Saves combined output to `data/processed/`

**Output Columns**: All match columns + enriched `odds_count` field containing list of available odds types per sport.

---

## 📊 Output Format

### Example: `matches_with_odds_2025-10-05_19-20-30.json`

```json
[
  {
    "sport_id": "basketball",
    "id": "12345",
    "home_team": "Lakers",
    "away_team": "Warriors",
    "start_time": "2025-10-06T19:00:00Z",
    "league": "NBA",
    "odds_count": ["Moneyline", "Spread", "Total"]
  },
  {
    "sport_id": "basketball",
    "id": "12346",
    "home_team": "Celtics",
    "away_team": "Heat",
    "start_time": "2025-10-06T20:30:00Z",
    "league": "NBA",
    "odds_count": ["Moneyline", "Spread", "Total"]
  }
]
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **401 Unauthorized / 403 Forbidden**

**Cause**: Expired or invalid authentication token.

**Solution**:

```bash
# Get a fresh token from HotStreak website and update both scripts
```

#### 2. **`curl_cffi` Import Error**

**Cause**: Package not installed or incompatible version.

**Solution**:

```bash
pip install --upgrade curl_cffi
```

#### 3. **No Data Folders Found**

**Cause**: Running `combine_data.py` before fetching data.

**Solution**:

```bash
# Run in order:
python src/fetch_matches.py
python src/fetch_categories.py
python src/combine_data.py
```

#### 4. **Empty JSON Files**

**Cause**: API returned no data or network issues.

**Solution**:

- Check your internet connection
- Verify the token is still valid
- Check if HotStreak API is accessible

#### 5. **Module Not Found Errors**

**Cause**: Virtual environment not activated or dependencies not installed.

**Solution**:

```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

---

## � Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include comments for complex logic

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Vikas Patel**

- GitHub: [@iamvikaspatel](https://github.com/iamvikaspatel)
- Repository: [opticOdds](https://github.com/iamvikaspatel/opticOdds)

---

## 🙏 Acknowledgments

- HotStreak for providing the API
- `curl_cffi` library for Cloudflare bypass capabilities
- The Python community for excellent data processing tools

---

## 📮 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/iamvikaspatel/opticOdds/issues)
3. Open a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages (if any)
   - Your environment (OS, Python version)

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**

---

## 🛡️ Error Handling

Each script includes:

- `try/except` blocks for API, JSON, and file operations
- Network and file permission validation
- Automatic directory creation
- Safe returns (`empty DataFrame` instead of crashes)

Examples:

```python
if not games:
    print("⚠️ No game data found in API response.")
    return pd.DataFrame()
```

and

```python
if df_matches.empty or df_categories.empty:
    print("⚠️ One of the datasets is empty. Skipping merge.")
```

---

## 🧾 Handling Missing / Incomplete Data

| Scenario                     | Behavior                        |
| ---------------------------- | ------------------------------- |
| Missing teams or league info | Defaults to `"Unknown"`         |
| Missing categories           | Stored as empty lists `[]`      |
| Empty API responses          | Returns empty JSON safely       |
| Missing folders              | Created automatically           |
| Invalid JSON                 | Gracefully skipped with warning |

The final combined file will always maintain consistent schema — even if some API responses are incomplete.

---

## 🧱 Code Quality and Documentation

- **PEP 8-compliant naming**
- **Docstrings and comments** for all major functions
- **Consistent section headers** (Configuration / Fetch / Save / Run)
- **Uniform success / warning / error messages**

Example:

```python
def fetch_matches():
    """Fetch matches safely and save to timestamped folder."""
```

---

## 🧩 Running Entire Pipeline at Once

You can automate the entire process using `main.py`:

```bash
python main.py
```

Example output:

```
🚀 Starting HotStreak data pipeline...
✅ 30 matches saved to data/raw/matches/2025-10-05_18-41-00/matches_raw.json
✅ 150 categories saved to data/raw/categories/2025-10-05_18-41-02/categories_raw.json
✅ Combined file saved → data/processed/matches_with_odds_2025-10-05_18-41-06.json
✅ Pipeline completed successfully.
```

---

## 🧩 Future Enhancements

- Add `.env` file to store tokens securely
- Integrate with a scheduler (Airflow / Prefect / CRON)
- Add unit tests for each function
- Log to file instead of console for audits

---
