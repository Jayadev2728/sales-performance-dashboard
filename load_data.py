import pandas as pd
from sqlalchemy import create_engine


# 1. Load the CSV

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# 2. Rename columns to match our Postgres table exactly.

df.columns = [
    "row_id", "order_id", "order_date", "ship_date", "ship_mode",
    "customer_id", "customer_name", "segment", "country", "city",
    "state", "postal_code", "region", "product_id", "category",
    "sub_category", "product_name", "sales", "quantity", "discount", "profit"
]


# 3. Convert date columns from text -> real datetime objects

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True)
df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed", dayfirst=True)


# 4. Connect to Postgres.

engine = create_engine("postgresql://postgres:password@localhost:5433/superstore_db")


# 5. Push the DataFrame into the 'orders' table we created.

df.to_sql("orders", engine, if_exists="append", index=False)

print(f"Loaded {len(df)} rows into 'orders' table successfully.")
