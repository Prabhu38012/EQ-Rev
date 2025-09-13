# Quick Commerce Agent with Gradio Interface

This project provides a Gradio interface for the Quick Commerce Agent system, allowing you to interact with the agent through a web UI instead of the command line.

## Features

1. **Chat Interface**: Chat with the agent using natural language queries
2. **Stock Allocation**: Allocate stock units to different cities based on sales data
3. **Low Stock Detection**: Identify cities with low stock levels that need restocking

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Gradio interface:
   ```
   python app.py
   ```

2. Open your browser and go to `http://localhost:7860` to access the interface

## Interface Tabs

### Chat Interface
- Chat with the agent using natural language
- Example queries:
  - "Allocate 1000 units of Baby Mosquito Net"
  - "Check for low stock situations"

### Stock Allocation
- Enter the number of units to allocate and the product name
- Get a proportional allocation of stock based on sales data

### Low Stock Detection
- Click the button to check for cities with low stock levels
- View cities and products that need restocking

## Data Files

- `data/sales.csv`: Contains sales data by city and product
- `data/inventory.csv`: Contains current inventory levels by city and product

## How It Works

The agent uses sales data to make intelligent decisions about stock allocation and identifies cities with low stock levels based on historical sales patterns.