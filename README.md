# Sales Performance Dashboard

An end-to-end data analytics project that pulls raw retail transaction data through a full pipeline — PostgreSQL for storage and analysis, Python for data engineering, Power BI for visualization, and an LLM-powered insight generator that auto-writes an executive summary from live data.

<img width="1401" height="751" alt="Sales_Dashoard" src="https://github.com/user-attachments/assets/770213a5-d8b0-4110-a658-2d5c8585a59e" />

## Overview

This project analyzes 9,994 orders from the Superstore retail dataset (2014–2017) to answer real business questions: Which regions and product lines drive the most profit? Where is the business losing money, and why? The dashboard combines SQL-driven analysis, interactive Power BI visuals, and an AI-generated executive summary that updates based on the underlying data.

## Tech Stack

| Layer | Tool |
|---|---|
| Database | PostgreSQL |
| Data Loading & Transformation | Python (Pandas, SQLAlchemy) |
| Analysis | SQL (CTEs, window functions, aggregations) |
| Visualization | Power BI Desktop |
| AI Insight Generation | Groq API (Llama 3.1 8B) |

## Project Structure

```
sales-performance-dashboard/
├── README.md
├── load_data.py           # Loads and cleans raw CSV, pushes into PostgreSQL
├── generate_insights.py   # Pulls aggregated data, generates AI executive summary
├── sql_queries.sql        # All analysis queries (regional sales, MoM growth, loss drivers)
├── dashboard_screenshot.png
└── insights.txt           # Latest AI-generated summary output
```

## Data Pipeline

1. **Extract** — Raw CSV (Superstore dataset, Kaggle) loaded and cleaned with Pandas, including handling of mixed date formats across rows.
2. **Load** — Cleaned data pushed into a PostgreSQL `orders` table via SQLAlchemy.
3. **Analyze** — SQL queries covering regional performance, month-over-month sales growth (via `LAG()` window functions), profit ranking (`RANK()`), and loss-driver diagnostics.
4. **Visualize** — Power BI Desktop connected directly to PostgreSQL, with DAX measures for dynamic KPIs (Total Sales, Total Profit, Profit Margin %) and an interactive region slicer.
5. **Summarize** — A Python script recomputes key aggregates, feeds them to an LLM, and generates a written executive summary — with totals pre-computed in Python (not left to the model) to guarantee factual accuracy.

## Key Insights

- **West region leads** in both total sales ($725K) and profit ($108K) — the strongest-performing region overall.
- **Copiers, Phones, and Accessories** are the most profitable sub-categories, together contributing over $142K in profit.
- **Excessive discounting is a major loss driver**: sub-categories like Binders and Appliances saw average discounts of 60–80% on their loss-making orders, well above the dataset's typical discount rate.
- **Three product lines are a net drag on the business overall** — Tables, Bookcases, and Supplies together lose approximately $22.4K, even after accounting for their profitable orders. Tables in particular loses money despite only moderate discounting, suggesting a separate cost or shipping margin issue worth investigating.

## Setup & Installation

1. Clone this repo and install dependencies:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary groq
   ```
2. Create a PostgreSQL database and run the schema from `sql_queries.sql` (or the `CREATE TABLE` statement at the top of the file).
3. Download the [Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place the CSV in the project folder.
4. In `load_data.py`, set your PostgreSQL connection string, then run:
   ```bash
   python load_data.py
   ```
5. In `generate_insights.py`, add your [Groq API key](https://console.groq.com) (free tier), then run:
   ```bash
   python generate_insights.py
   ```
6. Open the `.pbix` file in Power BI Desktop and refresh the data connection to point to your local database.

## Future Improvements

- Automate the pipeline end-to-end with a scheduler so the dashboard and AI summary refresh on a set cadence.
- Add customer-level segmentation (RFM analysis) as a companion analysis.
- Deploy the AI summary generation as a lightweight API so Power BI Service can trigger it directly.

## Author

**Jayadev H N**
GitHub: [github.com/Jayadev2728](https://github.com/Jayadev2728)
LinkedIn: [linkedin.com/in/jayadev-hn-8b1685326](https://linkedin.com/in/jayadev-hn-8b1685326)
Email: jayadevhn27@gmail.com
