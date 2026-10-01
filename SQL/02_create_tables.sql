USE retail_business_intelligence;

-- ============================================
-- 1. PRODUCT DIMENSION
-- ============================================

CREATE TABLE dim_product (
    ProductKey INT PRIMARY KEY,
    SKU VARCHAR(50),
    Product VARCHAR(255),
    Standard_Cost DECIMAL(12,4),
    Color VARCHAR(100),
    List_Price DECIMAL(12,4),
    Model VARCHAR(255),
    Subcategory VARCHAR(255),
    Category VARCHAR(100)
);

-- ============================================
-- 2. CUSTOMER DIMENSION
-- ============================================

CREATE TABLE dim_customer (
    CustomerKey INT PRIMARY KEY,
    Customer_ID VARCHAR(50),
    Customer VARCHAR(255),
    City VARCHAR(100),
    State_Province VARCHAR(100),
    Country_Region VARCHAR(100),
    Postal_Code VARCHAR(30)
);

-- ============================================
-- 3. RESELLER DIMENSION
-- ============================================

CREATE TABLE dim_reseller (
    ResellerKey INT PRIMARY KEY,
    Reseller_ID VARCHAR(50),
    Business_Type VARCHAR(100),
    Reseller VARCHAR(255),
    City VARCHAR(100),
    State_Province VARCHAR(100),
    Country_Region VARCHAR(100),
    Postal_Code VARCHAR(30)
);

-- ============================================
-- 4. TERRITORY DIMENSION
-- ============================================

CREATE TABLE dim_territory (
    SalesTerritoryKey INT PRIMARY KEY,
    Region VARCHAR(100),
    Country VARCHAR(100),
    `Group` VARCHAR(100)
);

-- ============================================
-- 5. DATE DIMENSION
-- ============================================

CREATE TABLE dim_date (
    DateKey INT PRIMARY KEY,
    `Date` DATE,
    Fiscal_Year VARCHAR(20),
    Fiscal_Quarter VARCHAR(20),
    Month VARCHAR(20),
    Full_Date VARCHAR(50),
    MonthKey INT
);

-- ============================================
-- 6. SALES FACT TABLE
-- ============================================

CREATE TABLE fact_sales (
    SalesOrderLineKey INT PRIMARY KEY,
    ResellerKey INT,
    CustomerKey INT,
    ProductKey INT,
    OrderDateKey INT,
    DueDateKey INT,
    ShipDateKey INT NULL,
    SalesTerritoryKey INT,
    Order_Quantity INT,
    Unit_Price DECIMAL(12,4),
    Extended_Amount DECIMAL(14,4),
    Unit_Price_Discount_Pct DECIMAL(10,4),
    Product_Standard_Cost DECIMAL(12,4),
    Total_Product_Cost DECIMAL(14,4),
    Sales_Amount DECIMAL(14,4),
    Order_Date DATE,
    Due_Date DATE,
    Ship_Date DATE NULL,
    Order_Year INT,
    Order_Month VARCHAR(20),
    Order_Month_Number INT,
    Order_Quarter VARCHAR(10),
    Order_Day INT,
    Order_Day_Name VARCHAR(20),
    Profit DECIMAL(14,4),
    Profit_Margin DECIMAL(10,4),
    Discount_Amount DECIMAL(14,4),
    Revenue_Per_Unit DECIMAL(14,4)
);

USE retail_business_intelligence;

SHOW TABLES;


USE retail_business_intelligence;

TRUNCATE TABLE fact_sales;

SELECT COUNT(*) AS sales_rows
FROM fact_sales;

SELECT COUNT(*) AS sales_rows
FROM retail_business_intelligence.fact_sales;