import pandas as pd

file_path = "../Data/AdventureWorks Sales.xlsx"

# Load workbook once
excel_file = pd.ExcelFile(file_path)

print("Loading data...")

# Load all required tables once
sales_order_df = pd.read_excel(file_path, sheet_name="Sales Order_data")
territory_df = pd.read_excel(file_path, sheet_name="Sales Territory_data")
sales_df = pd.read_excel(file_path, sheet_name="Sales_data")
reseller_df = pd.read_excel(file_path, sheet_name="Reseller_data")
date_df = pd.read_excel(file_path, sheet_name="Date_data")
product_df = pd.read_excel(file_path, sheet_name="Product_data")
customer_df = pd.read_excel(file_path, sheet_name="Customer_data")

# Store all tables in a dictionary
tables = {
    "Sales Order_data": sales_order_df,
    "Sales Territory_data": territory_df,
    "Sales_data": sales_df,
    "Reseller_data": reseller_df,
    "Date_data": date_df,
    "Product_data": product_df,
    "Customer_data": customer_df
}


# ============================================================
# TABLE SIZES
# ============================================================

print("\nTable sizes:")
print("=" * 50)

for sheet, df in tables.items():
    print(f"\n{sheet}:")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")


# ============================================================
# DATA QUALITY CHECKS
# ============================================================

print("\n\nData quality checks:")
print("=" * 50)

for sheet, df in tables.items():

    print(f"\n{sheet}")

    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("Missing values:")
    print(df.isnull().sum())


# ============================================================
# INVESTIGATING MISSING VALUES
# ============================================================

print("\n\nInvestigating missing values:")
print("=" * 50)

print("\nRows with missing ShipDateKey:")
print(
    sales_df[sales_df["ShipDateKey"].isnull()].head()
)

print("\nNumber of missing ShipDateKey values:")
print(
    sales_df["ShipDateKey"].isnull().sum()
)


print("\nProducts with missing Color:")
print(
    product_df[product_df["Color"].isnull()]
)

print("\nNumber of missing Color values:")
print(
    product_df["Color"].isnull().sum()
)


# ============================================================
# KEY UNIQUENESS CHECKS
# ============================================================

print("\n\nKey uniqueness checks:")
print("=" * 50)

key_checks = {

    "Sales_data.SalesOrderLineKey":
        sales_df["SalesOrderLineKey"],

    "Sales_Order_data.SalesOrderLineKey":
        sales_order_df["SalesOrderLineKey"],

    "Product_data.ProductKey":
        product_df["ProductKey"],

    "Customer_data.CustomerKey":
        customer_df["CustomerKey"],

    "Reseller_data.ResellerKey":
        reseller_df["ResellerKey"],

    "Sales_Territory_data.SalesTerritoryKey":
        territory_df["SalesTerritoryKey"],

    "Date_data.DateKey":
        date_df["DateKey"]
}


for name, column in key_checks.items():

    duplicate_count = column.duplicated().sum()
    unique_count = column.nunique()

    print(f"\n{name}")
    print(f"  Total values: {len(column):,}")
    print(f"  Unique values: {unique_count:,}")
    print(f"  Duplicate values: {duplicate_count:,}")
print("\nReferential integrity checks:")
print("=" * 50)

def check_foreign_key(sales_column, master_column, sales_df, master_df):
    sales_values = set(sales_df[sales_column].dropna())
    master_values = set(master_df[master_column].dropna())

    missing_values = sales_values - master_values

    print(f"\n{sales_column} → {master_column}")
    print(f"  Distinct values in Sales_data: {len(sales_values):,}")
    print(f"  Missing from master table: {len(missing_values):,}")

    if missing_values:
        print(f"  Example missing values: {list(missing_values)[:10]}")
    else:
        print("  Status: PASS")


check_foreign_key(
    "ProductKey",
    "ProductKey",
    sales_df,
    product_df
)

check_foreign_key(
    "CustomerKey",
    "CustomerKey",
    sales_df,
    customer_df
)

check_foreign_key(
    "ResellerKey",
    "ResellerKey",
    sales_df,
    reseller_df
)

check_foreign_key(
    "SalesTerritoryKey",
    "SalesTerritoryKey",
    sales_df,
    territory_df
)

check_foreign_key(
    "OrderDateKey",
    "DateKey",
    sales_df,
    date_df
)

check_foreign_key(
    "DueDateKey",
    "DateKey",
    sales_df,
    date_df
)

check_foreign_key(
    "ShipDateKey",
    "DateKey",
    sales_df,
    date_df
)

check_foreign_key(
    "SalesOrderLineKey",
    "SalesOrderLineKey",
    sales_df,
    sales_order_df
)  


print("\nExecutive KPIs:")
print("=" * 50)

# 1. Total Sales
total_sales = sales_df["Sales Amount"].sum()

# 2. Total Product Cost
total_cost = sales_df["Total Product Cost"].sum()

# 3. Total Profit
total_profit = total_sales - total_cost

# 4. Profit Margin
profit_margin = (total_profit / total_sales) * 100

# 5. Total Orders
total_orders = sales_order_df["Sales Order"].nunique()

# 6. Units Sold
units_sold = sales_df["Order Quantity"].sum()

# 7. Average Order Value
average_order_value = total_sales / total_orders

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Product Cost: ${total_cost:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Total Orders: {total_orders:,}")
print(f"Units Sold: {units_sold:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")

print("\nSales by Fiscal Year:")
print("=" * 50)



# Convert date keys to the same data type
sales_df["OrderDateKey"] = sales_df["OrderDateKey"].astype(int)
date_df["DateKey"] = date_df["DateKey"].astype(int)

# Join sales with date information
sales_with_date = sales_df.merge(
    date_df[["DateKey", "Fiscal Year", "Fiscal Quarter", "Month"]],
    left_on="OrderDateKey",
    right_on="DateKey",
    how="left"
)

# Sales by fiscal year
sales_by_year = (
    sales_with_date
    .groupby("Fiscal Year")["Sales Amount"]
    .sum()
    .reset_index()
)

print(sales_by_year.to_string(index=False))

print("\nFiscal Year Growth:")
print("=" * 50)

sales_by_year["YoY Growth %"] = (
    sales_by_year["Sales Amount"]
    .pct_change() * 100
)

print(sales_by_year.to_string(index=False))


print("\nSales date range:")
print("=" * 50)

print("Minimum OrderDateKey:", sales_df["OrderDateKey"].min())
print("Maximum OrderDateKey:", sales_df["OrderDateKey"].max())

print("\nDate table range:")
print("Minimum DateKey:", date_df["DateKey"].min())
print("Maximum DateKey:", date_df["DateKey"].max())


print("\nMonthly Sales:")
print("=" * 50)

sales_with_date["OrderDate"] = pd.to_datetime(
    sales_with_date["OrderDateKey"].astype(str)
)

sales_with_date["YearMonth"] = (
    sales_with_date["OrderDate"].dt.to_period("M")
)

monthly_sales = (
    sales_with_date
    .groupby("YearMonth")["Sales Amount"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)

monthly_sales["Sales Amount"] = monthly_sales["Sales Amount"].round(2)

print(monthly_sales.to_string(index=False))

print("\nMonthly Sales Analysis:")
print("=" * 50)

highest_month = monthly_sales.loc[
    monthly_sales["Sales Amount"].idxmax()
]

lowest_month = monthly_sales.loc[
    monthly_sales["Sales Amount"].idxmin()
]

print(
    f"Highest Sales Month: {highest_month['YearMonth']} "
    f"→ ${highest_month['Sales Amount']:,.2f}"
)

print(
    f"Lowest Sales Month: {lowest_month['YearMonth']} "
    f"→ ${lowest_month['Sales Amount']:,.2f}"
)

print("\nTop 5 Sales Months:")
print(
    monthly_sales
    .nlargest(5, "Sales Amount")
    .to_string(index=False)
)

print("\nBottom 5 Sales Months:")
print(
    monthly_sales
    .nsmallest(5, "Sales Amount")
    .to_string(index=False)
)

print("\nSales by Month of Year:")
print("=" * 50)

sales_with_date["Month_Name"] = sales_with_date["OrderDate"].dt.month_name()
sales_with_date["Month_Number"] = sales_with_date["OrderDate"].dt.month

seasonality = (
    sales_with_date
    .groupby(["Month_Number", "Month_Name"])["Sales Amount"]
    .sum()
    .reset_index()
    .sort_values("Month_Number")
)

print(seasonality.to_string(index=False))

print("\nAverage Sales by Month of Year:")
print("=" * 50)

# Create Year and Month columns
sales_with_date["Year"] = sales_with_date["OrderDate"].dt.year
sales_with_date["Month_Number"] = sales_with_date["OrderDate"].dt.month

# Calculate sales for each month in each year
monthly_year_sales = (
    sales_with_date
    .groupby(["Year", "Month_Number"])["Sales Amount"]
    .sum()
    .reset_index()
)

# Calculate the average sales for each calendar month
average_monthly_sales = (
    monthly_year_sales
    .groupby("Month_Number")["Sales Amount"]
    .mean()
    .reset_index()
)

# Add month names
average_monthly_sales["Month_Name"] = pd.to_datetime(
    average_monthly_sales["Month_Number"],
    format="%m"
).dt.month_name()

average_monthly_sales = average_monthly_sales.sort_values("Month_Number")

print(
    average_monthly_sales[
        ["Month_Number", "Month_Name", "Sales Amount"]
    ].to_string(index=False)
)

print("\nSales by Product Category:")
print("=" * 50)

product_sales = sales_df.merge(
    product_df[
        [
            "ProductKey",
            "SKU",
            "Product",
            "Model",
            "Subcategory",
            "Category"
        ]
    ],
    on="ProductKey",
    how="left"
)

category_analysis = (
    product_sales
    .groupby("Category")
    .agg(
        Sales=("Sales Amount", "sum"),
        Product_Cost=("Total Product Cost", "sum"),
        Units_Sold=("Order Quantity", "sum")
    )
    .reset_index()
)

category_analysis["Profit"] = (
    category_analysis["Sales"]
    - category_analysis["Product_Cost"]
)

category_analysis["Profit_Margin_%"] = (
    category_analysis["Profit"]
    / category_analysis["Sales"]
    * 100
)

category_analysis = category_analysis.sort_values(
    "Sales",
    ascending=False
)

print(category_analysis.to_string(index=False))

print("\nSales and Profit by Subcategory:")
print("=" * 50)

subcategory_analysis = (
    product_sales
    .groupby("Subcategory")
    .agg(
        Sales=("Sales Amount", "sum"),
        Product_Cost=("Total Product Cost", "sum"),
        Units_Sold=("Order Quantity", "sum")
    )
    .reset_index()
)

subcategory_analysis["Profit"] = (
    subcategory_analysis["Sales"]
    - subcategory_analysis["Product_Cost"]
)

subcategory_analysis["Profit_Margin_%"] = (
    subcategory_analysis["Profit"]
    / subcategory_analysis["Sales"]
    * 100
)

subcategory_analysis = subcategory_analysis.sort_values(
    "Sales",
    ascending=False
)

print(subcategory_analysis.to_string(index=False))

print("\nTop 10 Products by Sales (SKU Level):")
print("=" * 50)

product_analysis_sku = (
    product_sales
    .groupby(
        ["SKU", "Product", "Subcategory", "Category"]
    )
    .agg(
        Sales=("Sales Amount", "sum"),
        Product_Cost=("Total Product Cost", "sum"),
        Units_Sold=("Order Quantity", "sum")
    )
    .reset_index()
)

product_analysis_sku["Profit"] = (
    product_analysis_sku["Sales"]
    - product_analysis_sku["Product_Cost"]
)

product_analysis_sku["Profit_Margin_%"] = (
    product_analysis_sku["Profit"]
    / product_analysis_sku["Sales"]
    * 100
)

top_products_sku = (
    product_analysis_sku
    .sort_values("Sales", ascending=False)
    .head(10)
)

print(
    top_products_sku.to_string(index=False)
)

print("\nRepeated SKU / Product Combinations:")

print("=" * 50)

repeated_sku_product = (
    product_df[
        product_df.duplicated(
            ["SKU", "Product"],
            keep=False
        )
    ]
    .sort_values(
        ["SKU", "Product", "ProductKey"]
    )
)

print(
    repeated_sku_product[
        [
            "ProductKey",
            "SKU",
            "Product",
            "Model",
            "Subcategory",
            "Category"
        ]
    ].to_string(index=False)
)



print("\nSales and Profit by Product Model:")
print("=" * 50)

model_analysis = (
    product_sales
    .groupby("Model")
    .agg(
        Sales=("Sales Amount", "sum"),
        Product_Cost=("Total Product Cost", "sum"),
        Units_Sold=("Order Quantity", "sum")
    )
    .reset_index()
)

model_analysis["Profit"] = (
    model_analysis["Sales"]
    - model_analysis["Product_Cost"]
)

model_analysis["Profit_Margin_%"] = (
    model_analysis["Profit"]
    / model_analysis["Sales"]
    * 100
)

model_analysis = model_analysis.sort_values(
    "Sales",
    ascending=False
)

print(model_analysis.head(15).to_string(index=False))


print("\nSales and Profit by Channel:")
print("=" * 50)

sales_channel = sales_df.merge(
    sales_order_df[
        [
            "SalesOrderLineKey",
            "Channel"
        ]
    ],
    on="SalesOrderLineKey",
    how="left"
)

channel_analysis = (
    sales_channel
    .groupby("Channel")
    .agg(
        Sales=("Sales Amount", "sum"),
        Product_Cost=("Total Product Cost", "sum"),
        Units_Sold=("Order Quantity", "sum"),
        Sales_Lines=("SalesOrderLineKey", "nunique")
    )
    .reset_index()
)

channel_analysis["Profit"] = (
    channel_analysis["Sales"]
    - channel_analysis["Product_Cost"]
)

channel_analysis["Profit_Margin_%"] = (
    channel_analysis["Profit"]
    / channel_analysis["Sales"]
    * 100
)

print(
    channel_analysis.to_string(index=False)
)

print("\nChannel Contribution:")
print("=" * 50)

total_channel_sales = channel_analysis["Sales"].sum()
total_channel_profit = channel_analysis["Profit"].sum()

channel_analysis["Sales_Share_%"] = (
    channel_analysis["Sales"]
    / total_channel_sales
    * 100
)

channel_analysis["Profit_Share_%"] = (
    channel_analysis["Profit"]
    / total_channel_profit
    * 100
)

print(
    channel_analysis[
        [
            "Channel",
            "Sales",
            "Profit",
            "Profit_Margin_%",
            "Sales_Share_%",
            "Profit_Share_%"
        ]
    ].to_string(index=False)
)

print("\nChannel Order Analysis:")
print("=" * 50)

orders_by_channel = (
    sales_order_df
    .groupby("Channel")["Sales Order"]
    .nunique()
    .rename("Orders")
)

sales_by_channel = (
    sales_channel
    .groupby("Channel")
    .agg(
        Sales=("Sales Amount", "sum"),
        Units_Sold=("Order Quantity", "sum")
    )
)

channel_orders = pd.concat(
    [
        orders_by_channel,
        sales_by_channel
    ],
    axis=1
).reset_index()

channel_orders["Average_Order_Value"] = (
    channel_orders["Sales"]
    / channel_orders["Orders"]
)

channel_orders["Units_Per_Order"] = (
    channel_orders["Units_Sold"]
    / channel_orders["Orders"]
)

print(
    channel_orders.to_string(index=False)
)


