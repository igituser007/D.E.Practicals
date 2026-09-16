-- ============================================================
-- Practical 02: ETL into SQL Server - Data Warehouse Script
-- ============================================================
-- This is correct, standard T-SQL, written to run in SQL Server
-- Management Studio (SSMS) against a real SQL Server instance.
-- It could NOT be executed in this sandbox, since no SQL Server
-- engine is available here (see README.txt for details) - this is
-- the intended, correct code for you to run in your own SSMS.
--
-- It creates a small star-schema data warehouse (Sales_DW) with
-- dimension tables and a fact table, then loads it with sample data.
-- ============================================================

-- Step 1: Create the data warehouse database
IF DB_ID('Sales_DW') IS NULL
BEGIN
    CREATE DATABASE Sales_DW;
END
GO

USE Sales_DW;
GO

-- Step 2: Drop tables if they already exist (so this script can be
-- re-run cleanly)
IF OBJECT_ID('dbo.FactSales', 'U') IS NOT NULL DROP TABLE dbo.FactSales;
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL DROP TABLE dbo.DimCustomer;
IF OBJECT_ID('dbo.DimProduct', 'U') IS NOT NULL DROP TABLE dbo.DimProduct;
IF OBJECT_ID('dbo.DimDate', 'U') IS NOT NULL DROP TABLE dbo.DimDate;
GO

-- Step 3: Create dimension tables
CREATE TABLE dbo.DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    City VARCHAR(50)
);

CREATE TABLE dbo.DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50)
);

CREATE TABLE dbo.DimDate (
    DateKey INT PRIMARY KEY,       -- format YYYYMMDD
    FullDate DATE NOT NULL,
    Year INT,
    Month INT,
    MonthName VARCHAR(20)
);

-- Step 4: Create the fact table, linked to the dimensions above
CREATE TABLE dbo.FactSales (
    SaleID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerKey INT FOREIGN KEY REFERENCES dbo.DimCustomer(CustomerKey),
    ProductKey INT FOREIGN KEY REFERENCES dbo.DimProduct(ProductKey),
    DateKey INT FOREIGN KEY REFERENCES dbo.DimDate(DateKey),
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    Revenue AS (Quantity * UnitPrice) PERSISTED
);
GO

-- Step 5: Populate the dimensions (this is the "Load" part of ETL,
-- after data has been extracted and transformed from a source system)
INSERT INTO dbo.DimCustomer (CustomerName, City) VALUES
    ('Riya', 'Pune'),
    ('Amit', 'Mumbai'),
    ('Neha', 'Pune');

INSERT INTO dbo.DimProduct (ProductName, Category) VALUES
    ('Pen', 'Stationery'),
    ('Notebook', 'Stationery'),
    ('Mouse', 'Electronics');

INSERT INTO dbo.DimDate (DateKey, FullDate, Year, Month, MonthName) VALUES
    (20260105, '2026-01-05', 2026, 1, 'January'),
    (20260210, '2026-02-10', 2026, 2, 'February');

INSERT INTO dbo.FactSales (CustomerKey, ProductKey, DateKey, Quantity, UnitPrice) VALUES
    (1, 1, 20260105, 10, 10.00),
    (2, 2, 20260105, 5, 40.00),
    (3, 3, 20260210, 2, 700.00);
GO

-- Step 6: Example reporting query - total revenue by product category
SELECT
    p.Category,
    SUM(f.Revenue) AS TotalRevenue
FROM dbo.FactSales f
JOIN dbo.DimProduct p ON f.ProductKey = p.ProductKey
GROUP BY p.Category
ORDER BY TotalRevenue DESC;
GO
