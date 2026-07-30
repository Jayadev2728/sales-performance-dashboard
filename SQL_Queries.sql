CREATE TABLE orders (
    row_id INT,
    order_id VARCHAR(20),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(30),
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    segment VARCHAR(30),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(10),
    region VARCHAR(20),
    product_id VARCHAR(20),
    category VARCHAR(30),
    sub_category VARCHAR(30),
    product_name VARCHAR(200),
    sales NUMERIC(10,2),
    quantity INT,
    discount NUMERIC(4,2),
    profit NUMERIC(10,2)
);

SELECT * FROM orders LIMIT 5;

SELECT COUNT(*) FROM orders;


--Basic aggregation: Sales & Profit by Region

SELECT
    region,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    COUNT(*) AS total_orders
FROM orders
GROUP BY region
ORDER BY total_sales DESC;



--Month-over-Month Sales Growth

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(sales)::numeric AS total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    month,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(LAG(total_sales) OVER (ORDER BY month), 2) AS prev_month_sales,
    ROUND(
        ((total_sales - LAG(total_sales) OVER (ORDER BY month)) / LAG(total_sales) OVER (ORDER BY month)) * 100,
    2) AS mom_growth_pct
FROM monthly_sales
ORDER BY month;





--Top 10 Most Profitable Sub-Categories

SELECT
    sub_category,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM orders
GROUP BY sub_category
ORDER BY total_profit DESC
LIMIT 10;




--Loss-Making Orders

SELECT
    category,
    sub_category,
    COUNT(*) AS loss_making_orders,
    ROUND(SUM(profit)::numeric, 2) AS total_loss,
    ROUND(AVG(discount)::numeric * 100, 1) AS avg_discount_pct
FROM orders
WHERE profit < 0
GROUP BY category, sub_category
ORDER BY total_loss ASC
LIMIT 10;



SELECT
    sub_category,
    COUNT(*) AS total_orders,
    ROUND(AVG(profit)::numeric, 2) AS avg_profit,
    ROUND(AVG(discount)::numeric * 100, 1) AS avg_discount_pct
FROM orders
GROUP BY sub_category
ORDER BY avg_profit ASC
LIMIT 5;