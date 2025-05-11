# TikTok Virality Analysis

This project explores what makes TikTok videos go viral by collecting and analyzing video metadata such as titles, links, and engagement metrics. It includes a scraping script and preliminary data processing to build a dataset for future modeling or visualization.

---

## 📂 Project Overview

### 🎯 Goal
Identify key patterns or features (e.g., content type, keywords, engagement stats) that correlate with virality on TikTok.

---

## 🔍 Components

### `00f1c658-8244-4c54-9a47-1686231b5d06.js`
- JavaScript script used to scrape TikTok video titles and links directly from the browser.
- Steps:
  1. Scroll through the TikTok profile page to load videos.
  2. Extract video titles and links.
  3. Export the data as a `.csv` file for analysis.

### `84eead6b-4210-4b10-a7c5-c41665f38b2b.py`
- Python script (details not visible here) — assumed to handle:
  - Reading the scraped CSV
  - Cleaning and analyzing video metadata
  - Extracting features for statistical or machine learning modeling

---

## 🚀 How to Use

1. Open TikTok profile page in browser.
2. Paste and run the JavaScript (`.js`) in the browser console.
3. Download the generated CSV (`my_data.csv`).
4. Use the Python script to analyze the CSV file and explore patterns in video titles and virality.

---

## 🧠 Potential Analysis Directions

- Most common words in viral video titles
- Correlation between posting time and views
- Topic modeling or clustering based on description
- Predictive modeling to score virality likelihood

---

## 🛠 Tools & Tech

- JavaScript (browser-based scraping)
- Python (data cleaning and analysis)
- pandas, matplotlib, seaborn, sklearn (expected)

---

## 📌 Notes

- This project is exploratory and uses publicly available TikTok video metadata.
- No private data or user information is collected.

