import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

input_file = project_root / "Cleaned_Data" / "Sales_Fact.csv"
output_file = project_root / "Cleaned_Data" / "Sales_Fact_SQL.csv"

sales_fact = pd.read_csv(input_file)

print("Sales Fact loaded:", sales_fact.shape)

integer_columns = [
    "SalesOrderLineKey",
    "ResellerKey",
    "CustomerKey",
    "ProductKey",
    "OrderDateKey",
    "DueDateKey",
    "ShipDateKey",
    "SalesTerritoryKey",
    "Order_Quantity",
    "Order_Year",
    "Order_Month_Number",
    "Order_Day"
]

for column in integer_columns:
    sales_fact[column] = (
        pd.to_numeric(sales_fact[column], errors="coerce")
        .round()
        .astype("Int64")
    )

sales_fact.to_csv(output_file, index=False)

print("\nSQL EXPORT CREATED")
print("=" * 50)
print("File:", output_file)
print("Rows:", len(sales_fact))
print("Columns:", len(sales_fact.columns))
print("Missing ShipDateKey:", sales_fact["ShipDateKey"].isna().sum())