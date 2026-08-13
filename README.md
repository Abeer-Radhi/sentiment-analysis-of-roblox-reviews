# sentiment-analysis-of-roblox-reviews

## 1. Project Information
* **Project Name:** Roblox Player Sentiment & Feedback Pipeline
* **Team Members:** Abeer Radhi & Sarah Mohamed
* **Challenge Topics Used:** Web Scraping / Public APIs & Sentiment Analysis (NLP)
* **OpenCode Model Used:** Big Pickle (`opencode/big-pickle`) - Google

---

## 2. Problem Statement & Objectives
* **What We Built:** An automated Python data pipeline that scrapes public Google Play Store reviews for Roblox, processes raw feedback text using a pre-trained Transformer model (`RoBERTa`), maps sentiment categories, exports clean CSV datasets (`roblox_sentiment_reviews.csv`), and generates visualization charts (`sentiment_chart.png`).
* **Why This Idea:** Roblox hosts millions of active daily players who post thousands of reviews regarding game updates, server stability, microtransactions (Robux), and account bans. Manual review collection is impossible. Automating this feedback pipeline enables game developers and community managers to instantly capture true player sentiment, uncover top complaints, and make data-driven decisions to boost player retention.

---

## 3. Architecture & Flow

### Initial Plan (Pseudocode & Logic Flow)
```text
[ START ]
   │
   ├── 1. Fetch Google Play reviews for 'com.roblox.client' (limit = 100, lang = 'en')
   │
   ├── 2. Clean & Preprocess Review Text (Filter empty/non-string values)
   │
   ├── 3. Pass text through RoBERTa Sentiment Transformer Pipeline
   │
   ├── 4. Map Model Output Labels (label_0 -> negative, label_1 -> neutral, label_2 -> positive)
   │
   ├── 5. Export structured results to CSV (UTF-8-SIG encoded)
   │
   ├── 6. Generate Matplotlib Sentiment Distribution Bar Chart (sentiment_chart.png)
   │
   └── 7. Calculate & Print Executive Summary (Top words for Positive/Negative reviews)
   │

"""
## 4. Testing & Validation
* Initial API Validation: Tested data scraping with a small sample (50 records) before scaling to 100 review records to ensure clean connectivity and field extraction.
* Terminal & Unicode Validation: Forced UTF-8 stdout configuration (sys.stdout.reconfigure(encoding="utf-8")) to prevent Windows console crashes caused by non-ASCII review text and emojis.
* Label Mapping Verification: Validated model output dictionaries to verify that raw model predictions (label_0, label_1, label_2) correctly mapped to human-readable sentiment tags (negative, neutral, positive).

## 5. Limitations & Troubleshooting
* Target Dataset Misalignment (Steam to Google Play Pivot): Initial attempts to scrape Steam reviews using App ID 2132850 failed due to API payload mismatch/unavailability. We pivoted to the google-play-scraper package targeting Roblox's official package (com.roblox.client).
* Domain Slang & Model Upgrade: Rule-based models (like VADER) failed to recognize gaming jargon (lag, Robux, ban, scam). We instructed the agent to upgrade the engine to Hugging Face's cardiffnlp/twitter-roberta-base-sentiment-latest transformer model.
* PowerShell Command Syntax Errors: Pasting prompt strings containing ampersands (&) directly into the PowerShell terminal caused AmpersandNotAllowed parser errors. We resolved this by executing pure Python commands (python Main.py).
* Input Restrictions & Manual Oversight: Character thresholds and prompt limitations required structured instructions and manual supervision to correct agent logic bugs.

## 6. Coolest / Most Useful Agent Feature
* Rapid Script Execution & Auto-Debugging: The agent excelled at instantly generating the base project structure, setting up Matplotlib visualization functions, and embedding utf-8-sig encoding handling. It allowed us to transition seamlessly from scraping to full sentiment analysis in a fraction of the time.

## 7. Key Lessons Learned
* Start Small for Testing: Testing pipelines with small sample datasets first ensures fast iteration and validation before scaling up execution.
* Domain Slang Requires Advanced AI: Standard dictionary-based sentiment tools fail on gaming jargon (lag, Robux, pay-to-win); transformer models (RoBERTa) are essential for contextual accuracy.
* Developer Oversight is Essential: While AI agents write functional code fast, human oversight is critical to catch output mapping bugs (label_0 to negative), manage API rate limits, and resolve terminal syntax errors.
* Pivot When Blocked: Technical blockers (such as unlisted Steam IDs) require flexibility to adjust data sources without sacrificing project objectives.

## 8. Prompt Log (Summary)
| Stage | What Was Asked | Agent Output | Changes / Corrections Made |
| :--- | :--- | :--- | :--- |
| Data Fetching (Steam API) | Write a Python script to fetch 50 Roblox reviews from Steam API (App ID: 2132850) into a Pandas DataFrame. | Created fetch_roblox_reviews(limit=50) returning review_text, recommended, playtime_hours, and timestamp. | Fixed Windows UTF-8 terminal encoding. Tested and verified execution. |
| Data Source Pivot (Google Play) | Switch data source to fetch public Google Play Store reviews for com.roblox.client due to Steam API mapping issues. | Replaced Steam API logic with google-play-scraper fetching recent English reviews. | Updated DataFrame structure to support Play Store rating scores and text content. |
| AI Model Upgrade | Replace basic sentiment analysis with Gemini AI / Hugging Face RoBERTa transformer (cardiffnlp/twitter-roberta-base-sentiment-latest). | Integrated Hugging Face pipeline, updated CSV saving to roblox_sentiment_reviews.csv, and generated sentiment_chart.png. | Added explicit label mapping (label_0, label_1, label_2 -> negative, neutral, positive) to fix chart calculation bugs. |
| Execution & Terminal Cleanup | Resolve PowerShell AmpersandNotAllowed error when running Main.py. | Advised running script directly via clean PowerShell command. | Executed python Main.py successfully in Terminal. |

The link: https://opncd.ai/share/o4AzeX9a

"""

[ END ]
