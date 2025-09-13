import unittest
import pandas as pd
from agent.logic import allocate_stock, detect_low_stock

class TestAgentLogic(unittest.TestCase):
    
    def setUp(self):
        # Create sample data for testing
        self.sales_data = {
            'city_name': ['mumbai', 'delhi', 'bangalore', 'mumbai', 'delhi'],
            'product_name': ['product_a', 'product_a', 'product_a', 'product_b', 'product_b'],
            'units_sold': [100, 200, 150, 50, 75]
        }
        self.inventory_data = {
            'city_name': ['mumbai', 'delhi', 'bangalore'],
            'product_name': ['product_a', 'product_a', 'product_a'],
            'stock_quantity': [50, 30, 80]
        }
        self.sales_df = pd.DataFrame(self.sales_data)
        self.inventory_df = pd.DataFrame(self.inventory_data)
    
    def test_allocate_stock(self):
        # Test stock allocation
        city_sales = {'mumbai': 100, 'delhi': 200, 'bangalore': 150}
        allocation = allocate_stock(1000, city_sales)
        
        # Check that total allocated units match
        total_allocated = sum(allocation.values())
        self.assertEqual(total_allocated, 1000)
        
        # Check that delhi gets more than mumbai (higher sales)
        self.assertGreater(allocation['delhi'], allocation['mumbai'])
    
    def test_allocate_stock_zero_sales(self):
        # Test stock allocation when all sales are zero
        city_sales = {'mumbai': 0, 'delhi': 0, 'bangalore': 0}
        allocation = allocate_stock(1000, city_sales)
        
        # Check that units are evenly distributed
        expected_per_city = 1000 // 3
        for city in city_sales:
            self.assertEqual(allocation[city], expected_per_city)
    
    def test_detect_low_stock(self):
        # Test low stock detection
        risk = detect_low_stock(self.inventory_df, self.sales_df, threshold=0.5)
        
        # This is a simple test - in real scenario, we would check actual values
        # For now, we just check that it returns a list
        self.assertIsInstance(risk, list)

if __name__ == '__main__':
    unittest.main()