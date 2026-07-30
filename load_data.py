import pandas as pd
from sqlalchemy import create_engine

# ---------------------------------------------------------
# 1. Load the CSV
#    encoding="latin1" avoids UnicodeDecodeError -- this
#    dataset has a few special characters (accented names)
#    that plain utf-8 can't read.
# ---------------------------------------------------------
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# ---------------------------------------------------------
# 2. Rename columns to match our Postgres table exactly.
#    The CSV has headers like "Row ID", "Order Date" (with
#    spaces/capitals) -- Postgres columns are snake_case.
#    Order below matches the CSV's column order exactly.
# ---------------------------------------------------------
df.columns = [
    "row_id", "order_id", "order_date", "ship_date", "ship_mode",
    "customer_id", "customer_name", "segment", "country", "city",
    "state", "postal_code", "region", "product_id", "category",
    "sub_category", "product_name", "sales", "quantity", "discount", "profit"
]

# ---------------------------------------------------------
# 3. Convert date columns from text -> real datetime objects
#    so Postgres stores them as DATE, not VARCHAR.
# ---------------------------------------------------------
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True)
df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed", dayfirst=True)

# ---------------------------------------------------------
# 4. Connect to Postgres.
#    Connection string format:
#    postgresql://username:password@host:port/database_name
#    !! Replace YOUR_PASSWORD with the password you set
#    !! during PostgreSQL installation.
# ---------------------------------------------------------
engine = create_engine("postgresql://postgres:password@localhost:5433/superstore_db")

# ---------------------------------------------------------
# 5. Push the DataFrame into the 'orders' table we created.
#    if_exists="append" -> adds rows to the existing empty table
#    (we already defined the schema with CREATE TABLE, so we
#    don't want Pandas to guess/create its own column types)
# ---------------------------------------------------------
df.to_sql("orders", engine, if_exists="append", index=False)

print(f"Loaded {len(df)} rows into 'orders' table successfully.")
