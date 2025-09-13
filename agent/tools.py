from langchain.tools import tool
import pandas as pd
from agent.logic import allocate_stock, detect_low_stock
import json

# Load data
sales_df = pd.read_csv("data/sales.csv")
inventory_df = pd.read_csv("data/inventory.csv")

@tool
def allocate_stock_tool(input_str: str) -> str:
    """
    Allocate given units based on past 7-day sales.
    Expected input: JSON string {"units": 1000, "product": "ProductX"}.
    """
    data = json.loads(input_str)
    product = data['product']
    units = data['units']
    
    # Get sales data for the product
    product_sales = sales_df[sales_df['product'] == product]
    city_sales = product_sales.groupby('city')['sales'].sum().to_dict()
    
    allocation = allocate_stock(units, city_sales)
    # Removed n8n webhook trigger
    return f"Stock allocation complete: {allocation}"

@tool
def low_stock_tool(input_str: str = "") -> str:
    """
    Detect cities needing urgent restocking. Input is ignored.
    """
    risk = detect_low_stock(inventory_df, sales_df)
    if not risk:
        return "No cities currently at risk."
    
    # Removed n8n webhook trigger
    return f"Cities at risk: {risk}"