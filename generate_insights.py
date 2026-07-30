import pandas as pd
from sqlalchemy import create_engine, text
from groq import Groq

# ---------------------------------------------------------
# 1. Connect to your Postgres database
#    (same connection details as load_data.py)
# ---------------------------------------------------------
engine = create_engine("postgresql://postgres:PASSWORD@localhost:5433/superstore_db")

# ---------------------------------------------------------
# 2. Pull the key aggregated numbers we already validated
#    in Step 6 (SQL) and Step 8 (Power BI). We're reusing
#    the same logic so the AI's summary matches what's
#    actually on your dashboard.
# ---------------------------------------------------------
with engine.connect() as conn:
    region_sales = pd.read_sql(text("""
        SELECT region, ROUND(SUM(sales)::numeric, 2) AS total_sales,
               ROUND(SUM(profit)::numeric, 2) AS total_profit
        FROM orders GROUP BY region ORDER BY total_sales DESC
    """), conn)

    top_subcats = pd.read_sql(text("""
        SELECT sub_category, ROUND(SUM(profit)::numeric, 2) AS total_profit
        FROM orders GROUP BY sub_category ORDER BY total_profit DESC LIMIT 3
    """), conn)

    losing_subcats = pd.read_sql(text("""
        SELECT sub_category, ROUND(SUM(profit)::numeric, 2) AS total_profit
        FROM orders GROUP BY sub_category
        HAVING SUM(profit) < 0 ORDER BY total_profit ASC
    """), conn)

    overall = pd.read_sql(text("""
        SELECT ROUND(SUM(sales)::numeric, 2) AS total_sales,
               ROUND(SUM(profit)::numeric, 2) AS total_profit,
               COUNT(*) AS total_orders
        FROM orders
    """), conn)

# ---------------------------------------------------------
# 3. Build a clear, data-grounded prompt.
#    We feed the AI our OWN validated numbers -- it's
#    writing up findings, not inventing them.
# ---------------------------------------------------------
# Pre-compute the loss total ourselves -- never let the LLM
# do arithmetic on numbers we can calculate exactly in Python.
total_losses = round(losing_subcats["total_profit"].sum(), 2)

prompt = f"""
You are a data analyst writing a short executive summary for a sales dashboard.
Use ONLY the numbers provided below. Do not invent any figures, and do not
recalculate any totals yourself -- use the pre-computed totals exactly as given.

Overall: {overall.to_dict('records')[0]}
Sales & profit by region: {region_sales.to_dict('records')}
Top 3 most profitable sub-categories: {top_subcats.to_dict('records')}
Sub-categories that are a net loss overall: {losing_subcats.to_dict('records')}
Pre-computed total of these losses (use this exact number): {total_losses}

Write a 4-5 sentence executive summary highlighting:
1. Overall performance
2. The best-performing region
3. The strongest product sub-categories
4. The sub-categories dragging down profit, and a brief suggestion
Keep it business-toned, concise, and suitable to paste directly onto a dashboard.
"""

# ---------------------------------------------------------
# 4. Call Groq's free API (OpenAI-compatible client)
# ---------------------------------------------------------
client = Groq(api_key="API_KEY")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)

insight_text = response.choices[0].message.content

# ---------------------------------------------------------
# 5. Save it so you can paste it into Power BI / README
# ---------------------------------------------------------
with open("insights.txt", "w") as f:
    f.write(insight_text)

print("Generated insight:\n")
print(insight_text)
print("\nSaved to insights.txt")