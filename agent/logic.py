import pandas as pd

def allocate_stock(units, city_sales):
    """
    Allocate stock proportionally based on recent sales.
    :param units: Total units to allocate.
    :param city_sales: Dictionary {city: total_sales}.
    :return: Dictionary {city: allocated_units}.
    """
    total_sales = sum(city_sales.values())
    if total_sales == 0:
        # Evenly split if no sales data
        return {city: units // len(city_sales) for city in city_sales}
    
    allocation = {}
    allocated_total = 0
    
    # Calculate proportional allocation for all cities except the last one
    cities = list(city_sales.keys())
    for i, city in enumerate(cities):
        if i == len(cities) - 1:
            # Last city gets the remaining units to ensure total is exactly 'units'
            allocation[city] = units - allocated_total
        else:
            city_units = int((city_sales[city] / total_sales) * units)
            allocation[city] = city_units
            allocated_total += city_units
            
    return allocation

def detect_low_stock(inventory_df, sales_df, threshold=0.2):
    """
    Detect cities where current inventory < threshold * avg 3-day sales.
    :param inventory_df: DataFrame with columns [city_name, product_name, stock_quantity]
    :param sales_df: DataFrame with columns [city_name, product_name, units_sold]
    :return: List of tuples [(city, product, current_stock, avg_sales)]
    """
    risk = []
    
    # Calculate average sales per product per city
    avg_sales = sales_df.groupby(['city_name', 'product_name'])['units_sold'].mean().reset_index()
    
    # Merge with inventory data
    merged = pd.merge(inventory_df, avg_sales, on=['city_name', 'product_name'], how='left')
    merged['units_sold'] = merged['units_sold'].fillna(0)
    
    # Check for low stock
    for _, row in merged.iterrows():
        if row['stock_quantity'] < threshold * row['units_sold']:
            risk.append((row['city_name'], row['product_name'], row['stock_quantity'], row['units_sold']))
    
    return risk