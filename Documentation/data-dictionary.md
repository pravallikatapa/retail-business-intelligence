\## 1. Sales\_Order\_data



\### Purpose



Contains sales order and sales order line identifiers, along with the sales channel.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| Channel | Sales channel such as Internet or Reseller | Attribute |

| SalesOrderLineKey | Unique identifier for each sales order line | Primary Key |

| Sales Order | Identifier of the overall sales order | Relationship/Reference |

| Sales Order Line | Identifier describing the individual line within an order | Attribute |



\### Important Observation



One Sales Order can contain multiple Sales Order Lines.



Example:

SO43659 → SO43659 - 1, SO43659 - 2, SO43659 - 3, etc.



\### Approximate Row Count



Approximately 121,253 data rows based on the displayed worksheet.





\## 2. Sales\_Territory\_data



\### Purpose



Contains geographic information used to classify sales territories into regions, countries, and broader geographic groups.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| SalesTerritoryKey | Unique identifier for each sales territory | Primary Key |

| Region | Name of the sales territory or region | Attribute |

| Country | Country associated with the territory | Attribute |

| Group | Broader geographic grouping | Attribute |



\### Geographic Hierarchy



Group → Country → Region



\### Example



North America → United States → Northwest

Europe → France → France



\### Approximate Row Count



11 data rows.



\## 3. Sales\_data



\### Purpose



Contains individual sales transaction lines, including channel information, customers/resellers, products, dates, territory, quantity, pricing, discounts, product cost, and sales amount.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| SalesOrderLineKey | Unique identifier for each sales order line | Primary Key |

| ResellerKey | Identifies the reseller for reseller-channel sales | Foreign Key |

| CustomerKey | Identifies the customer for internet-channel sales | Foreign Key |

| ProductKey | Identifies the product sold | Foreign Key |

| OrderDateKey | Key representing the order date | Foreign Key |

| DueDateKey | Key representing the due date | Foreign Key |

| ShipDateKey | Key representing the shipping date | Foreign Key |

| SalesTerritoryKey | Identifies the sales territory | Foreign Key |

| Order Quantity | Number of units in the order line | Measure |

| Unit Price | Selling price per unit | Measure |

| Extended Amount | Quantity multiplied by unit price | Measure |

| Unit Price Discount Pct | Discount percentage applied to the unit price | Measure |

| Product Standard Cost | Standard cost per unit | Measure |

| Total Product Cost | Total standard product cost for the order line | Measure |

| Sales Amount | Sales value recorded for the order line | Measure |



\### Important Business Logic



\- Reseller-channel sales use ResellerKey while CustomerKey is -1.

\- Internet-channel sales use CustomerKey while ResellerKey is -1.

\- One sales order can contain multiple sales order lines.

\- One sales order line can contain multiple units of the same product.

\- OrderDateKey, DueDateKey, and ShipDateKey use a YYYYMMDD date-key format.



\### Potential Derived Metric



Gross Margin based on Standard Product Cost:



Sales Amount - Total Product Cost



This should not be interpreted as net profit because the dataset does not contain all business expenses.



\## 4. Reseller\_data



\### Purpose



Contains information about businesses that resell AdventureWorks products, including their business type and geographic location.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| ResellerKey | Unique internal identifier for each reseller | Primary Key |

| Reseller ID | Business/reference identifier for the reseller | Identifier |

| Business Type | Type of reseller business | Attribute |

| Reseller | Name of the reseller business | Attribute |

| City | City where the reseller is located | Attribute |

| State-Province | State or province where the reseller is located | Attribute |

| Country-Region | Country or region where the reseller is located | Attribute |

| Postal Code | Postal/ZIP code of the reseller | Attribute |



\### Important Observation



ResellerKey = -1 represents Not Applicable and is used when a sale does not have an associated reseller, such as an Internet-channel sale.



\### Potential Business Questions



\- Which reseller generates the highest sales?

\- Which reseller business type generates the most sales?

\- Which countries have the highest reseller sales?

\- Which reseller locations perform best?





\## 5. Date\_data



\### Purpose



Contains calendar and fiscal-date information used to support time-based sales analysis and reporting.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| DateKey | Unique numeric identifier for each date in YYYYMMDD format | Primary Key |

| Date | Calendar date | Attribute |

| Fiscal Year | Company's fiscal year associated with the date | Attribute |

| Fiscal Quarter | Fiscal quarter associated with the date | Attribute |

| Month | Year and month label | Attribute |

| Full Date | Readable date representation | Attribute |

| MonthKey | Numeric identifier representing year and month | Attribute |



\### Date Range



Approximately July 1, 2017 to June 30, 2021.



\### Fiscal Year



The fiscal year begins in July.



Example:



July 2017 → FY2018 Q1



\### Important Relationships



Sales\_data.OrderDateKey → Date\_data.DateKey



Sales\_data.DueDateKey → Date\_data.DateKey



Sales\_data.ShipDateKey → Date\_data.DateKey



\### Potential Business Questions



\- How do sales change month by month?

\- Which fiscal year generated the highest sales?

\- Which fiscal quarter performed best?

\- What are the monthly sales trends?

\- How does performance change year over year?





\## 6. Product\_data



\### Purpose



Contains product master information including product identifiers, SKU, pricing, cost, color, model, subcategory, and category.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| ProductKey | Unique identifier for a product record | Primary Key |

| SKU | Stock Keeping Unit/business product code | Identifier |

| Product | Specific product name/description | Attribute |

| Standard Cost | Standard cost per unit | Measure |

| Color | Product color | Attribute |

| List Price | Listed price of the product | Measure |

| Model | Product model | Attribute |

| Subcategory | Specific product grouping | Attribute |

| Category | Broad product grouping | Attribute |



\### Product Hierarchy



Category → Subcategory → Model → Product



\### Important Observation



ProductKey is used to connect Product\_data with Sales\_data.



SKU should not automatically be treated as a unique key because the dataset contains repeated SKU values.



\### Potential Business Questions



\- Which product categories generate the most sales?

\- Which subcategories perform best?

\- Which products generate the highest sales?

\- Which products have the highest gross margin based on standard product cost?

\- Which models perform best?

\- Which products have the highest order quantities?



\## 7. Customer\_data



\### Purpose



Contains customer master information including customer identifiers, names, and geographic information.



\### Columns



| Column | Description | Key/Role |

|---|---|---|

| CustomerKey | Unique internal identifier for each customer | Primary Key |

| Customer ID | Business/customer identifier | Identifier |

| Customer | Customer name | Attribute |

| City | Customer's city | Attribute |

| State-Province | Customer's state or province | Attribute |

| Country-Region | Customer's country or region | Attribute |

| Postal Code | Customer's postal/ZIP code | Attribute |



\### Important Observation



CustomerKey = -1 represents Not Applicable and is used for sales that do not have an associated direct customer, such as reseller-channel sales.



\### Relationship



Sales\_data.CustomerKey → Customer\_data.CustomerKey



\### Potential Business Questions



\- Which customers generate the highest sales?

\- Which countries have the highest customer sales?

\- Which regions have the highest customer concentration?

\- What are the characteristics of high-value customers?







\# Data Relationships

\## Fact Table



Sales\_data is the central fact table containing individual sales transactions.



\## Relationships



Sales\_data.SalesOrderLineKey

→ Sales\_Order\_data.SalesOrderLineKey



Sales\_data.ProductKey

→ Product\_data.ProductKey



Sales\_data.CustomerKey

→ Customer\_data.CustomerKey



Sales\_data.ResellerKey

→ Reseller\_data.ResellerKey



Sales\_data.SalesTerritoryKey

→ Sales\_Territory\_data.SalesTerritoryKey



Sales\_data.OrderDateKey

→ Date\_data.DateKey



Sales\_data.DueDateKey

→ Date\_data.DateKey



Sales\_data.ShipDateKey

→ Date\_data.DateKey



\## Row Counts



| Table | Rows | Columns |

|---|---:|---:|

| Sales\_data | 121,253 | 15 |

| Sales\_Order\_data | 121,253 | 4 |

| Customer\_data | 18,485 | 7 |

| Product\_data | 397 | 9 |

| Reseller\_data | 702 | 8 |

| Date\_data | 1,461 | 7 |

| Sales\_Territory\_data | 11 | 4 |





\# Business Requirements \& KPIs



\## Project Objective



Analyze AdventureWorks sales data to evaluate revenue, profitability,

customer behavior, product performance, sales channels, geographic

performance, and operational efficiency, and provide actionable insights

to support management decision-making.



\## Stakeholders



\- CEO / Business Manager

\- Sales Manager

\- Product Manager

\- Operations Manager



\## Key Business Questions



\### Sales Performance

1\. What is total sales revenue?

2\. How does revenue change over time?

3\. Which periods perform best and worst?

4\. How much profit is generated?

5\. What is the overall profit margin?



\### Product Performance

6\. Which categories generate the most revenue?

7\. Which subcategories perform best?

8\. Which products generate the most revenue?

9\. Which products have the highest profit margins?



\### Customer Performance

10\. Which customers generate the most revenue?

11\. Which countries/regions generate the most customer sales?

12\. How concentrated is revenue among high-value customers?



\### Channel Performance

13\. How do Internet and Reseller sales compare?

14\. Which channel generates more revenue?

15\. Which channel has better profitability?

16\. How has channel performance changed over time?



\### Geographic Performance

17\. Which territories generate the most revenue?

18\. Which territories generate the most profit?

19\. Are there high-revenue but low-margin territories?



\### Operational Performance

20\. What percentage of sales records have no ship date?

21\. How long does shipping take when dates are available?

22\. Does shipping performance vary by channel or territory?



\---



\# KPI Definitions



| KPI | Definition |

|---|---|

| Total Sales | SUM(Sales Amount) |

| Total Profit | SUM(Sales Amount - Total Product Cost) |

| Profit Margin % | Total Profit / Total Sales × 100 |

| Total Orders | DISTINCT COUNT(Sales Order) |

| Units Sold | SUM(Order Quantity) |

| Average Order Value | Total Sales / Total Orders |

| Unique Customers | DISTINCT COUNT(CustomerKey), excluding -1 where appropriate |

| Channel Revenue % | Channel Sales / Total Sales × 100 |

| Missing Ship Date % | Missing ShipDateKey / Total Sales Lines × 100 |

| Average Shipping Days | Average(Ship Date - Order Date) where both dates exist |



\## Primary Executive KPIs



1\. Total Sales

2\. Total Profit

3\. Profit Margin %

4\. Total Orders

5\. Units Sold

6\. Average Order Value





\## Data Coverage



The Date\_data table covers July 1, 2017 through June 30, 2021.



However, Sales\_data contains OrderDateKey values only from July 1, 2017

through June 15, 2020.



Therefore:



\- FY2018: Full fiscal year available

\- FY2019: Full fiscal year available

\- FY2020: Partial fiscal year, ending June 15, 2020

\- FY2021: No sales transactions available



FY2020 comparisons should therefore be interpreted with caution because

the fiscal year is not complete.

