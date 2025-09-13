import gradio as gr
import pandas as pd
import json
from agent.direct_handler import handle_query
from agent.logic import allocate_stock, detect_low_stock

# Load data
try:
    sales_df = pd.read_csv("data/sales.csv")
    inventory_df = pd.read_csv("data/inventory.csv")
except FileNotFoundError as e:
    raise FileNotFoundError(f"Required data files not found. Please ensure data/sales.csv and data/inventory.csv exist. Error: {e}")

def process_query(query):
    """
    Process the user query and return the response
    """
    try:
        response = handle_query(query)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def allocate_stock_interface(units, product):
    """
    Interface for stock allocation
    """
    try:
        if not product:
            return "Please enter a product name."
        
        if units <= 0:
            return "Please enter a valid number of units (> 0)."
            
        # Get sales data for the product
        product_sales = sales_df[sales_df['product_name'].str.contains(product, case=False, na=False)]
        if product_sales.empty:
            return f"No sales data found for product containing: {product}"
        
        city_sales = product_sales.groupby('city_name')['units_sold'].sum().to_dict()
        allocation = allocate_stock(int(units), city_sales)
        
        # Format the result for better display
        result_str = "Stock allocation:\n"
        for city, units_allocated in allocation.items():
            result_str += f"{city}: {units_allocated} units\n"
            
        return result_str
    except Exception as e:
        return f"Error processing allocation: {str(e)}"

def low_stock_interface():
    """
    Interface for low stock detection
    """
    try:
        risk = detect_low_stock(inventory_df, sales_df)
        if not risk:
            return "No cities currently at risk."
        
        result_str = "Cities at risk:\n"
        for city, product, current_stock, avg_sales in risk:
            result_str += f"{city} - {product}: Current stock {current_stock}, Avg sales {avg_sales:.2f}\n"
            
        return result_str
    except Exception as e:
        return f"Error checking stock levels: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Quick Commerce Agent") as demo:
    gr.Markdown("# Quick Commerce Agent")
    gr.Markdown("This interface allows you to interact with the Quick Commerce Agent system.")
    
    with gr.Tab("Chat Interface"):
        gr.Markdown("### Chat with the Agent")
        chatbot = gr.Chatbot(label="Conversation")
        msg = gr.Textbox(label="Your Query", placeholder="Ask about stock allocation or low stock detection...")
        clear = gr.Button("Clear")
        
        def respond(message, chat_history):
            bot_message = process_query(message)
            chat_history.append((message, bot_message))
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)
    
    with gr.Tab("Stock Allocation"):
        gr.Markdown("### Allocate Stock")
        units = gr.Number(label="Units to Allocate", value=1000, precision=0)
        product = gr.Textbox(label="Product Name", placeholder="Enter product name...")
        allocate_btn = gr.Button("Allocate Stock")
        allocation_output = gr.Textbox(label="Allocation Result", lines=10)
        
        allocate_btn.click(allocate_stock_interface, inputs=[units, product], outputs=allocation_output)
    
    with gr.Tab("Low Stock Detection"):
        gr.Markdown("### Check for Low Stock")
        low_stock_btn = gr.Button("Check Low Stock")
        low_stock_output = gr.Textbox(label="Low Stock Result", lines=10)
        
        low_stock_btn.click(low_stock_interface, inputs=[], outputs=low_stock_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)