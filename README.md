# sentiment-analysis-of-roblox-reviews

## 1. Project Information
* **Project Name:** Roblox Player Sentiment & Feedback Pipeline
* **Team Members:** Abeer Radhi & Sarah Mohamed
* **Challenge Topics Used:** Web Scraping / Public APIs & Sentiment Analysis (NLP)
* **OpenCode Model Used:** Big Pickle (`opencode/big-pickle`)

---

## 2. Problem Statement & Objectives
* **What We Built:** An automated Python data pipeline that scrapes public Google Play Store reviews for Roblox, processes raw feedback text using a pre-trained Transformer model (`RoBERTa`), maps sentiment categories, exports clean CSV datasets (`roblox_sentiment_reviews.csv`), and generates visualization charts (`sentiment_chart.png`).
* **Why This Idea:** Roblox hosts millions of active daily players who post thousands of reviews regarding game updates, server stability, microtransactions (Robux), and account bans. Manual review collection is impossible. Automating this feedback pipeline enables game developers and community managers to instantly capture true player sentiment, uncover top complaints, and make data-driven decisions to boost player retention.

---

## 3. Architecture & Flow

### Initial Plan vs. Final Architecture

#### 1. Initial Concept (Exploratory Phase)
When starting out without knowing the exact model requirements, the initial plan relied on a simple rule-based approach (**VADER** sentiment analyzer) paired with Steam API fetching.


[ INITIAL EXPLORATORY FLOW ]
   └── 1. Fetch Steam Reviews (App ID: 2132850)
   
   └── 2. Run VADER Rule-Based Sentiment Analysis
   
   └── 3. Export Basic Polarity Scores

#### 2. Final Architecture (Upgraded Pipeline)
Upon inspecting early test outputs, we discovered VADER failed to understand gaming slang (lag, Robux, ban, scam), and Steam's API payload had mapping issues. We pivoted the data source and upgraded the NLP engine:

[ FINAL PIPELINE FLOW ]
   ├── 1. Fetch Google Play reviews for 'com.roblox.client' (limit = 100, lang = 'en')
   ├── 2. Clean & Preprocess Review Text
   ├── 3. Process text using RoBERTa Transformer ('cardiffnlp/twitter-roberta-base-sentiment-latest')
   ├── 4. Map Model Labels (label_0 -> negative, label_1 -> neutral, label_2 -> positive)
   ├── 5. Export structured results to CSV ('roblox_sentiment_reviews.csv' with UTF-8-SIG)
   ├── 6. Generate Matplotlib Sentiment Distribution Chart ('sentiment_chart.png')
   └── 7. Output Executive Terminal Summary (Top keywords for Positive & Negative feedback)

[ END ]

---

## 4. Testing & Validation
* **Initial API Validation:** Tested data scraping with a small sample (50 records) before scaling to 100 review records to ensure clean connectivity and field extraction.
* **Terminal & Unicode Validation:** Forced UTF-8 stdout configuration (`sys.stdout.reconfigure(encoding="utf-8")`) to prevent Windows console crashes caused by non-ASCII review text and emojis.
* **Label Mapping Verification:** Validated model output dictionaries to verify that raw model predictions (`label_0`, `label_1`, `label_2`) correctly mapped to human-readable sentiment tags (`negative`, `neutral`, `positive`).

---

## 5. Limitations & Troubleshooting
* **Target Dataset Misalignment (Steam to Google Play Pivot):** Initial attempts to scrape Steam reviews using App ID `2132850` failed due to API payload mismatch/unavailability. We pivoted to the `google-play-scraper` package targeting Roblox's official package (`com.roblox.client`).
* **Model Evaluation & Upgrade (VADER to RoBERTa):** Standard rule-based models (like VADER) failed on domain slang (*lag, Robux, ban, scam*). After reviewing the output accuracy, we instructed the agent to upgrade the engine to Hugging Face's `cardiffnlp/twitter-roberta-base-sentiment-latest` transformer model.
* **PowerShell Command Syntax Errors:** Pasting prompt strings containing ampersands (`&`) directly into the PowerShell terminal caused `AmpersandNotAllowed` parser errors. We resolved this by executing pure Python commands (`python Main.py`).
* **Input Restrictions & Manual Oversight:** Character thresholds and prompt limitations required structured instructions and manual supervision to correct agent logic bugs.

---

## 6. Coolest / Most Useful Agent Feature
* **Rapid Script Execution & Auto-Debugging:** The agent excelled at instantly generating the base project structure, setting up Matplotlib visualization functions, and embedding `utf-8-sig` encoding handling. It allowed us to transition seamlessly from scraping to full sentiment analysis in a fraction of the time.

---

## 7. Key Lessons Learned
* **Start Small for Testing:** Testing pipelines with small sample datasets first ensures fast iteration and validation before scaling up execution.
* **Evaluate and Upgrade Models Based on Data:** Starting with a simple model (VADER) helped us understand the baseline, but domain slang required upgrading to a Transformer model (RoBERTa) for contextual accuracy.
* **Developer Oversight is Essential:** While AI agents write functional code fast, human oversight is critical to catch output mapping bugs (`label_0` to `negative`), manage API rate limits, and resolve terminal syntax errors.
* **Pivot When Blocked:** Technical blockers (such as unlisted Steam IDs) require flexibility to adjust data sources without sacrificing project objectives.

---

## 8. Prompt Log

| Stage | What Was Asked | Agent Output | Changes / Corrections Made |
| :--- | :--- | :--- | :--- |
| **Data Fetching (Steam API)** | Write a Python script to fetch 50 Roblox reviews from Steam API (`App ID: 2132850`) into a Pandas DataFrame. | Created `fetch_roblox_reviews(limit=50)` returning `review_text`, `recommended`, `playtime_hours`, and `timestamp`. | Fixed Windows UTF-8 terminal encoding. Tested and verified execution. |
| **Data Source Pivot (Google Play)** | Switch data source to fetch public Google Play Store reviews for `com.roblox.client` due to Steam API mapping issues. | Replaced Steam API logic with `google-play-scraper` fetching recent English reviews. | Updated DataFrame structure to support Play Store rating scores and text content. |
| **Model Evaluation & Upgrade** | Replace initial VADER model with Hugging Face RoBERTa transformer (`cardiffnlp/twitter-roberta-base-sentiment-latest`) to capture gaming slang. | Integrated Hugging Face pipeline, updated CSV saving to `roblox_sentiment_reviews.csv`, and generated `sentiment_chart.png`. | Added explicit label mapping (`label_0`, `label_1`, `label_2` -> `negative`, `neutral`, `positive`) to fix chart calculation bugs. || **Execution & Terminal Cleanup** | Resolve PowerShell `AmpersandNotAllowed` error when running Main.py. | Advised running script directly via clean PowerShell command. | Executed `python Main.py` successfully in Terminal. |

The link of prompt log: https://opncd.ai/share/o4AzeX9a

Thank your for reading!
