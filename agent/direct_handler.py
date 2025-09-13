import pandas as pd
import json
from agent.logic import allocate_stock, detect_low_stock

# Load data
sales_df = pd.read_csv("data/sales.csv")
inventory_df = pd.read_csv("data/inventory.csv")

def handle_query(query):
    """
    Directly handle queries without using LangChain agent framework
    """
    query = query.lower()
    
    # Handle stock allocation
    if "allocate" in query and "units" in query:
        try:
            # Extract units and product from query
            words = query.split()
            units = None
            product = None
            
            for i, word in enumerate(words):
                if word.isdigit():
                    units = int(word)
                elif word == "of" and i + 1 < len(words):
                    product = words[i + 1]
                    break
            
            if units and product:
                # Get sales data for the product
                product_sales = sales_df[sales_df['product'] == product]
                if product_sales.empty:
                    return f"No sales data found for product: {product}"
                
                city_sales = product_sales.groupby('city')['sales'].sum().to_dict()
                allocation = allocate_stock(units, city_sales)
                return f"Stock allocation complete: {allocation}"
            else:
                return "Please specify both units and product, e.g., 'Allocate 1000 units of ProductX'"
        except Exception as e:
            return f"Error processing allocation: {str(e)}"
    
    # Handle low stock detection
    elif any(keyword in query for keyword in ["low stock", "restock", "urgent", "need stock"]):
        try:
            risk = detect_low_stock(inventory_df, sales_df)
            if not risk:
                return "No cities currently at risk."
            return f"Cities at risk: {risk}"
        except Exception as e:
            return f"Error checking stock levels: {str(e)}"
    
    # Handle unknown queries
    else:
        return "I can help with stock allocation and low stock detection. Try asking about allocating stock or checking for low stock situations."