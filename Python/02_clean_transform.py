import pandas as pd
from pathlib import Path


# ============================================
# 1. LOAD DATA
# ============================================

# Project folder
project_path = Path(
    r"C:\Users\prava\OneDrive\Documents\Projects BI\retail-business-intelligence"
)

# Excel file
file_path = project_path / "Data" / "AdventureWorks Sales.xlsx"


# Load all required tables
sales_order_df = pd.read_excel(
    file_path,
    sheet_name="Sales Order_data"
)

sales_territory_df = pd.read_excel(
    file_path,
    sheet_name="Sales Territory_data"
)

sales_df = pd.read_excel(
    file_path,
    sheet_name="Sales_data"
)

reseller_df = pd.read_excel(
    file_path,
    sheet_name="Reseller_data"
)

date_df = pd.read_excel(
    file_path,
    sheet_name="Date_data"
)

product_df = pd.read_excel(
    file_path,
    sheet_name="Product_data"
)

customer_df = pd.read_excel(
    file_path,
    sheet_name="Customer_data"
)


# ============================================
# 2. BASIC INFORMATION
# ============================================

print("\nDATA LOADED SUCCESSFULLY")
print("=" * 50)

print("\nSales Order:")
print(sales_order_df.shape)

print("\nSales Territory:")
print(sales_territory_df.shape)

print("\nSales:")
print(sales_df.shape)

print("\nReseller:")
print(reseller_df.shape)

print("\nDate:")
print(date_df.shape)

print("\nProduct:")
print(product_df.shape)

print("\nCustomer:")
print(customer_df.shape)

# ============================================
# 3. COLUMN AND DATA TYPE INSPECTION
# ============================================

tables = {
    "Sales Order": sales_order_df,
    "Sales Territory": sales_territory_df,
    "Sales": sales_df,
    "Reseller": reseller_df,
    "Date": date_df,
    "Product": product_df,
    "Customer": customer_df
}


for table_name, df in tables.items():

    print("\n" + "=" * 60)
    print(f"{table_name.upper()} TABLE")
    print("=" * 60)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)


    # ============================================
# 4. STANDARDIZE COLUMN NAMES
# ============================================

for df in tables.values():

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )


print("\nCOLUMN NAMES STANDARDIZED")
print("=" * 50)

for table_name, df in tables.items():

    print(f"\n{table_name}:")
    print(df.columns.tolist())

# ============================================
# 5. CHECK MISSING VALUES
# ============================================

print("\nMISSING VALUE CHECK")
print("=" * 50)

for table_name, df in tables.items():

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    print(f"\n{table_name}:")

    if missing.empty:
        print("No missing values")
    else:
        print(missing)

# ============================================
# 6. HANDLE MISSING VALUES
# ============================================

# Product Color
product_df["Color"] = product_df["Color"].fillna("Unknown")


# ShipDateKey
# Keep missing values because the actual shipping date is unknown.
# We will handle valid ShipDateKey values during date transformation.


print("\nMISSING VALUES HANDLED")
print("=" * 50)

print("\nProduct Color missing values:")
print(product_df["Color"].isnull().sum())

print("\nSales ShipDateKey missing values:")
print(sales_df["ShipDateKey"].isnull().sum())


# ============================================
# 7. CONVERT DATE KEYS TO ACTUAL DATES
# ============================================

# Create lookup dictionaries from the Date table

date_lookup = date_df.set_index("DateKey")["Date"]


# Convert OrderDateKey
sales_df["Order_Date"] = sales_df["OrderDateKey"].map(date_lookup)


# Convert DueDateKey
sales_df["Due_Date"] = sales_df["DueDateKey"].map(date_lookup)


# Convert ShipDateKey
# Missing ShipDateKey values will remain missing.
sales_df["Ship_Date"] = sales_df["ShipDateKey"].map(date_lookup)


print("\nDATE TRANSFORMATION")
print("=" * 50)

print("\nOrder Date:")
print(sales_df["Order_Date"].head())

print("\nDue Date:")
print(sales_df["Due_Date"].head())

print("\nShip Date:")
print(sales_df["Ship_Date"].head())


print("\nMissing transformed dates:")

print(
    "Order_Date:",
    sales_df["Order_Date"].isnull().sum()
)

print(
    "Due_Date:",
    sales_df["Due_Date"].isnull().sum()
)

print(
    "Ship_Date:",
    sales_df["Ship_Date"].isnull().sum()
)

# ============================================
# 8. CREATE TIME ATTRIBUTES
# ============================================

sales_df["Order_Year"] = sales_df["Order_Date"].dt.year

sales_df["Order_Month"] = sales_df["Order_Date"].dt.month_name()

sales_df["Order_Month_Number"] = sales_df["Order_Date"].dt.month

sales_df["Order_Quarter"] = (
    "Q" + sales_df["Order_Date"].dt.quarter.astype(str)
)

sales_df["Order_Day"] = sales_df["Order_Date"].dt.day

sales_df["Order_Day_Name"] = (
    sales_df["Order_Date"].dt.day_name()
)


print("\nTIME ATTRIBUTES CREATED")
print("=" * 50)

print(
    sales_df[
        [
            "Order_Date",
            "Order_Year",
            "Order_Month",
            "Order_Month_Number",
            "Order_Quarter",
            "Order_Day",
            "Order_Day_Name"
        ]
    ].head(10).to_string(index=False)
)

# ============================================
# 9. CREATE BUSINESS METRICS
# ============================================

# Profit
sales_df["Profit"] = (
    sales_df["Sales_Amount"]
    - sales_df["Total_Product_Cost"]
)


# Profit Margin
sales_df["Profit_Margin"] = (
    sales_df["Profit"]
    / sales_df["Sales_Amount"]
    * 100
)


# Discount Amount
sales_df["Discount_Amount"] = (
    sales_df["Unit_Price"]
    * sales_df["Order_Quantity"]
    * sales_df["Unit_Price_Discount_Pct"]
    / 100
)


# Revenue per Unit
sales_df["Revenue_Per_Unit"] = (
    sales_df["Sales_Amount"]
    / sales_df["Order_Quantity"]
)


print("\nBUSINESS METRICS CREATED")
print("=" * 50)

print(
    sales_df[
        [
            "Sales_Amount",
            "Total_Product_Cost",
            "Profit",
            "Profit_Margin",
            "Discount_Amount",
            "Revenue_Per_Unit"
        ]
    ].head(10).to_string(index=False)
)

# ============================================
# 10. VALIDATE BUSINESS METRICS
# ============================================

print("\nBUSINESS METRIC VALIDATION")
print("=" * 50)

print("\nMissing Profit values:")
print(sales_df["Profit"].isnull().sum())

print("\nMissing Profit Margin values:")
print(sales_df["Profit_Margin"].isnull().sum())

print("\nNegative Profit rows:")
print((sales_df["Profit"] < 0).sum())

print("\nZero Sales Amount rows:")
print((sales_df["Sales_Amount"] == 0).sum())

print("\nProfit summary:")
print(sales_df["Profit"].describe())


# ============================================
# 11. FINAL SALES TABLE VALIDATION
# ============================================

print("\nFINAL SALES TABLE VALIDATION")
print("=" * 50)

print("\nOriginal Sales row count:")
print(121253)

print("\nCurrent Sales row count:")
print(len(sales_df))

print("\nSales row count preserved:")
print(len(sales_df) == 121253)


print("\nDate mapping validation:")

print(
    "Order_Date missing:",
    sales_df["Order_Date"].isnull().sum()
)

print(
    "Due_Date missing:",
    sales_df["Due_Date"].isnull().sum()
)

print(
    "Ship_Date missing:",
    sales_df["Ship_Date"].isnull().sum()
)


print("\nSales Amount summary:")
print(
    sales_df["Sales_Amount"].describe()
)


print("\nTotal Sales:")
print(
    round(sales_df["Sales_Amount"].sum(), 2)
)


print("\nTotal Product Cost:")
print(
    round(sales_df["Total_Product_Cost"].sum(), 2)
)


print("\nTotal Profit:")
print(
    round(sales_df["Profit"].sum(), 2)
)

# ============================================
# 12. CREATE SALES FACT TABLE
# ============================================

sales_fact_df = sales_df.copy()


print("\nSALES FACT TABLE CREATED")
print("=" * 50)

print("\nRows:")
print(len(sales_fact_df))

print("\nColumns:")
print(sales_fact_df.columns.tolist())

print("\nShape:")
print(sales_fact_df.shape)

# ============================================
# 13. CREATE PRODUCT DIMENSION
# ============================================

product_dim_df = product_df[
    [
        "ProductKey",
        "SKU",
        "Product",
        "Standard_Cost",
        "Color",
        "List_Price",
        "Model",
        "Subcategory",
        "Category"
    ]
].copy()


print("\nPRODUCT DIMENSION CREATED")
print("=" * 50)

print("\nRows:")
print(len(product_dim_df))

print("\nColumns:")
print(product_dim_df.columns.tolist())

print("\nShape:")
print(product_dim_df.shape)

print("\nProductKey unique:")
print(product_dim_df["ProductKey"].is_unique)

# ============================================
# 14. CREATE CUSTOMER DIMENSION
# ============================================

customer_dim_df = customer_df[
    [
        "CustomerKey",
        "Customer_ID",
        "Customer",
        "City",
        "State_Province",
        "Country_Region",
        "Postal_Code"
    ]
].copy()


print("\nCUSTOMER DIMENSION CREATED")
print("=" * 50)

print("\nRows:")
print(len(customer_dim_df))

print("\nColumns:")
print(customer_dim_df.columns.tolist())

print("\nShape:")
print(customer_dim_df.shape)

print("\nCustomerKey unique:")
print(customer_dim_df["CustomerKey"].is_unique)

# ============================================
# 15. CREATE RESELLER DIMENSION
# ============================================

reseller_dim_df = reseller_df[
    [
        "ResellerKey",
        "Reseller_ID",
        "Business_Type",
        "Reseller",
        "City",
        "State_Province",
        "Country_Region",
        "Postal_Code"
    ]
].copy()


print("\nRESELLER DIMENSION CREATED")
print("=" * 50)

print("\nRows:")
print(len(reseller_dim_df))

print("\nColumns:")
print(reseller_dim_df.columns.tolist())

print("\nShape:")
print(reseller_dim_df.shape)

print("\nResellerKey unique:")
print(reseller_dim_df["ResellerKey"].is_unique)

# ============================================
# 16. CREATE TERRITORY DIMENSION
# ============================================

territory_dim_df = sales_territory_df[
    [
        "SalesTerritoryKey",
        "Region",
        "Country",
        "Group"
    ]
].copy()


print("\nTERRITORY DIMENSION CREATED")
print("=" * 50)

print("\nRows:")
print(len(territory_dim_df))

print("\nColumns:")
print(territory_dim_df.columns.tolist())

print("\nShape:")
print(territory_dim_df.shape)

print("\nSalesTerritoryKey unique:")
print(territory_dim_df["SalesTerritoryKey"].is_unique)

# ============================================
# 17. CREATE DATE DIMENSION
# ============================================

date_dim_df = date_df[
    [
        "DateKey",
        "Date",
        "Fiscal_Year",
        "Fiscal_Quarter",
        "Month",
        "Full_Date",
        "MonthKey"
    ]
].copy()


print("\nDATE DIMENSION CREATED")
print("=" * 50)

print("\nRows:")
print(len(date_dim_df))

print("\nColumns:")
print(date_dim_df.columns.tolist())

print("\nShape:")
print(date_dim_df.shape)

print("\nDateKey unique:")
print(date_dim_df["DateKey"].is_unique)

print("\nDate range:")
print(
    date_dim_df["Date"].min(),
    "to",
    date_dim_df["Date"].max()
)

# ============================================
# 18. FINAL STAR SCHEMA VALIDATION
# ============================================

print("\nFINAL STAR SCHEMA VALIDATION")
print("=" * 50)


# Product relationship
product_check = sales_fact_df["ProductKey"].isin(
    product_dim_df["ProductKey"]
).all()

print("\nProductKey relationship:")
print("PASS" if product_check else "FAIL")


# Customer relationship
customer_check = sales_fact_df["CustomerKey"].isin(
    customer_dim_df["CustomerKey"]
).all()

print("\nCustomerKey relationship:")
print("PASS" if customer_check else "FAIL")


# Reseller relationship
reseller_check = sales_fact_df["ResellerKey"].isin(
    reseller_dim_df["ResellerKey"]
).all()

print("\nResellerKey relationship:")
print("PASS" if reseller_check else "FAIL")


# Territory relationship
territory_check = sales_fact_df["SalesTerritoryKey"].isin(
    territory_dim_df["SalesTerritoryKey"]
).all()

print("\nSalesTerritoryKey relationship:")
print("PASS" if territory_check else "FAIL")


# Date relationship
date_check = sales_fact_df["OrderDateKey"].isin(
    date_dim_df["DateKey"]
).all()

print("\nOrderDateKey relationship:")
print("PASS" if date_check else "FAIL")


# Due date relationship
due_date_check = sales_fact_df["DueDateKey"].isin(
    date_dim_df["DateKey"]
).all()

print("\nDueDateKey relationship:")
print("PASS" if due_date_check else "FAIL")


# Ship date relationship
# Ignore missing ShipDateKey values.
ship_date_check = sales_fact_df.loc[
    sales_fact_df["ShipDateKey"].notna(),
    "ShipDateKey"
].isin(
    date_dim_df["DateKey"]
).all()

print("\nShipDateKey relationship:")
print("PASS" if ship_date_check else "FAIL")


# Overall result
all_relationships_valid = all(
    [
        product_check,
        customer_check,
        reseller_check,
        territory_check,
        date_check,
        due_date_check,
        ship_date_check
    ]
)

print("\nOverall Star Schema Validation:")
print("PASS" if all_relationships_valid else "FAIL")


# ============================================
# 19. EXPORT CLEANED TABLES
# ============================================

# Create output folder
output_path = project_path / "Cleaned_Data"

output_path.mkdir(
    parents=True,
    exist_ok=True
)


# Export Sales Fact
sales_fact_df.to_csv(
    output_path / "Sales_Fact.csv",
    index=False
)


# Export Product Dimension
product_dim_df.to_csv(
    output_path / "Product_Dim.csv",
    index=False
)


# Export Customer Dimension
customer_dim_df.to_csv(
    output_path / "Customer_Dim.csv",
    index=False
)


# Export Reseller Dimension
reseller_dim_df.to_csv(
    output_path / "Reseller_Dim.csv",
    index=False
)


# Export Territory Dimension
territory_dim_df.to_csv(
    output_path / "Territory_Dim.csv",
    index=False
)


# Export Date Dimension
date_dim_df.to_csv(
    output_path / "Date_Dim.csv",
    index=False
)


print("\nCLEANED TABLES EXPORTED")
print("=" * 50)

print("\nOutput folder:")
print(output_path)

print("\nFiles created:")
print("Sales_Fact.csv")
print("Product_Dim.csv")
print("Customer_Dim.csv")
print("Reseller_Dim.csv")
print("Territory_Dim.csv")
print("Date_Dim.csv")