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
    return {city: int((sales / total_sales) * units) for city, sales in city_sales.items()}

def detect_low_stock(inventory_df, sales_df, threshold=0.2):
    """
    Detect cities where current inventory < threshold * avg 3-day sales.
    :param inventory_df: DataFrame with columns [city, product, inventory]
    :param sales_df: DataFrame with columns [city, product, sales, date]
    :return: List of tuples [(city, product, current_stock, avg_sales)]
    """
    risk = []
    
    # Calculate average sales per product per city
    avg_sales = sales_df.groupby(['city', 'product'])['sales'].mean().reset_index()
    
    # Merge with inventory data
    merged = pd.merge(inventory_df, avg_sales, on=['city', 'product'], how='left')
    merged['avg_sales'] = merged['sales'].fillna(0)
    
    # Check for low stock
    for _, row in merged.iterrows():
        if row['inventory'] < threshold * row['avg_sales']:
            risk.append((row['city'], row['product'], row['inventory'], row['avg_sales']))
    
    return risk