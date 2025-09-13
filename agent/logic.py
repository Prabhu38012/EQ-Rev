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
        return {city: units // len(city_sales) for city in city_sales}  # evenly split
    return {city: int((sales / total_sales) * units) for city, sales in city_sales.items()}

def detect_low_stock(inventory_df, sales_df, threshold=0.2):
    """
    Detect cities where current inventory < threshold * avg 3-day sales.
    :param inventory_df: DataFrame with columns [city, product, inventory]
    :param sales_df: DataFrame with columns [city, product, sales, date]
    :return: List of tuples [(city, product, current_stock, avg_sales)]
    """
    risk = []
    # Calculate recent sales (last 3 days)
    recent_sales = sales_df.groupby(['city', 'product'])['sales'].sum().reset_index()
    
    for _, row in inventory_df.iterrows():
        city, product, inventory = row['city'], row['product'], row['inventory']
        product_sales = recent_sales[
            (recent_sales['city'] == city) & 
            (recent_sales['product'] == product)
        ]
        avg_sales = product_sales['sales'].mean() if not product_sales.empty else 0
        if inventory < threshold * avg_sales:
            risk.append((city, product, inventory, avg_sales))
    return risk