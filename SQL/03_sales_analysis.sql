
USE retail_business_intelligence;

-- 1. Overall Business Performance
SELECT
    COUNT(*) AS Sales_Records,
    SUM(Order_Quantity) AS Units_Sold,
    SUM(Sales_Amount) AS Total_Revenue,
    SUM(Total_Product_Cost) AS Total_Cost,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales_Amount) * 100, 2) AS Profit_Margin_Pct
FROM fact_sales;


-- 2. Revenue and Profit by Year
SELECT
    Order_Year,
    SUM(Sales_Amount) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales_Amount) * 100, 2) AS Profit_Margin_Pct
FROM fact_sales
GROUP BY Order_Year
ORDER BY Order_Year;


-- 3. Revenue and Profit by Product Category
SELECT
    p.Category,
    SUM(f.Sales_Amount) AS Total_Revenue,
    SUM(f.Profit) AS Total_Profit,
    SUM(f.Order_Quantity) AS Units_Sold,
    ROUND(SUM(f.Profit) / SUM(f.Sales_Amount) * 100, 2) AS Profit_Margin_Pct
FROM fact_sales f
JOIN dim_product p
    ON f.ProductKey = p.ProductKey
GROUP BY p.Category
ORDER BY Total_Revenue DESC;


-- 4. Top 10 Products by Revenue
SELECT
    p.SKU,
    p.Product,
    p.Subcategory,
    p.Category,
    SUM(f.Sales_Amount) AS Total_Revenue,
    SUM(f.Profit) AS Total_Profit,
    SUM(f.Order_Quantity) AS Units_Sold,
    ROUND(SUM(f.Profit) / SUM(f.Sales_Amount) * 100, 2) AS Profit_Margin_Pct
FROM fact_sales f
JOIN dim_product p
    ON f.ProductKey = p.ProductKey
GROUP BY
    p.SKU,
    p.Product,
    p.Subcategory,
    p.Category
ORDER BY Total_Revenue DESC
LIMIT 10;


-- 5. Revenue and Profit by Region
SELECT
    t.Region,
    SUM(f.Sales_Amount) AS Total_Revenue,
    SUM(f.Profit) AS Total_Profit,
    ROUND(SUM(f.Profit) / SUM(f.Sales_Amount) * 100, 2) AS Profit_Margin_Pct
FROM fact_sales f
JOIN dim_territory t
    ON f.SalesTerritoryKey = t.SalesTerritoryKey
GROUP BY t.Region
ORDER BY Total_Revenue DESC;


-- 6. Monthly Revenue and Profit Trend
SELECT
    Order_Year,
    Order_Month_Number,
    Order_Month,
    SUM(Sales_Amount) AS Total_Revenue,
    SUM(Profit) AS Total_Profit
FROM fact_sales
GROUP BY
    Order_Year,
    Order_Month_Number,
    Order_Month
ORDER BY
    Order_Year,
    Order_Month_Number;