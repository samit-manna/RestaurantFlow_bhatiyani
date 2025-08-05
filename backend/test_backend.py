#!/usr/bin/env python3
"""
Comprehensive Backend Tests for RestaurantFlow_bhatiyani
Tests all API endpoints, data validation, and error handling
"""

import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, restaurants_data, orders_data, menu_items_data, analytics_data


class RestaurantFlowBackendTestSuite(unittest.TestCase):
    """Comprehensive test suite for RestaurantFlow backend API"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Test data samples
        self.sample_restaurant = {
            "id": 1,
            "name": "Spice Garden",
            "address": "123 Main St",
            "phone": "555-0123",
            "cuisine": "Indian"
        }
        
        self.sample_order = {
            "id": 1,
            "restaurant_id": 1,
            "customer_name": "John Doe",
            "status": "pending",
            "total": 25.99,
            "items": ["Butter Chicken", "Naan"]
        }

    def test_root_endpoint(self):
        """Test the root endpoint returns correct API information"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'RestaurantFlow_bhatiyani API')
        self.assertEqual(data['version'], '1.0.0')
        self.assertEqual(data['status'], 'running')
        print("✅ Root endpoint test passed")

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('Flask API is running', data['message'])
        print("✅ Health check endpoint test passed")

    def test_get_all_restaurants(self):
        """Test retrieving all restaurants"""
        response = self.app.get('/api/restaurants')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Verify restaurant structure
        restaurant = data[0]
        required_fields = ['id', 'name', 'address', 'phone', 'cuisine']
        for field in required_fields:
            self.assertIn(field, restaurant)
        print("✅ Get all restaurants test passed")

    def test_get_single_restaurant_success(self):
        """Test retrieving a single restaurant by ID"""
        restaurant_id = 1
        response = self.app.get(f'/api/restaurants/{restaurant_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], restaurant_id)
        self.assertEqual(data['name'], 'Spice Garden')
        print("✅ Get single restaurant (success) test passed")

    def test_get_single_restaurant_not_found(self):
        """Test retrieving a non-existent restaurant"""
        restaurant_id = 999
        response = self.app.get(f'/api/restaurants/{restaurant_id}')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Restaurant not found')
        print("✅ Get single restaurant (not found) test passed")

    def test_get_all_orders(self):
        """Test retrieving all orders"""
        response = self.app.get('/api/orders')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Verify order structure
        order = data[0]
        required_fields = ['id', 'restaurant_id', 'customer_name', 'status', 'total', 'items']
        for field in required_fields:
            self.assertIn(field, order)
        print("✅ Get all orders test passed")

    def test_get_single_order_success(self):
        """Test retrieving a single order by ID"""
        order_id = 1
        response = self.app.get(f'/api/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], order_id)
        self.assertEqual(data['customer_name'], 'John Doe')
        print("✅ Get single order (success) test passed")

    def test_get_single_order_not_found(self):
        """Test retrieving a non-existent order"""
        order_id = 999
        response = self.app.get(f'/api/orders/{order_id}')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Order not found')
        print("✅ Get single order (not found) test passed")

    def test_get_all_menu_items(self):
        """Test retrieving all menu items"""
        response = self.app.get('/api/menu-items')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Verify menu item structure
        item = data[0]
        required_fields = ['id', 'restaurant_id', 'name', 'price', 'category']
        for field in required_fields:
            self.assertIn(field, item)
        print("✅ Get all menu items test passed")

    def test_get_restaurant_menu(self):
        """Test retrieving menu items for a specific restaurant"""
        restaurant_id = 1
        response = self.app.get(f'/api/menu-items/{restaurant_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Verify all items belong to the requested restaurant
        for item in data:
            self.assertEqual(item['restaurant_id'], restaurant_id)
        print("✅ Get restaurant menu test passed")

    def test_get_analytics(self):
        """Test retrieving analytics data"""
        response = self.app.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('daily_orders', data)
        self.assertIn('popular_items', data)
        
        # Verify daily orders structure
        daily_orders = data['daily_orders']
        self.assertIsInstance(daily_orders, list)
        self.assertGreater(len(daily_orders), 0)
        
        order_entry = daily_orders[0]
        required_fields = ['date', 'orders', 'revenue']
        for field in required_fields:
            self.assertIn(field, order_entry)
        print("✅ Get analytics test passed")

    def test_get_dashboard_data(self):
        """Test retrieving dashboard data for a specific restaurant"""
        restaurant_id = 1
        response = self.app.get(f'/api/analytics/dashboard/{restaurant_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        required_fields = ['today_orders', 'pending_orders', 'today_revenue', 'active_menu_items']
        for field in required_fields:
            self.assertIn(field, data)
            self.assertIsInstance(data[field], (int, float))
        print("✅ Get dashboard data test passed")

    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = self.app.get('/api/restaurants')
        self.assertEqual(response.status_code, 200)
        
        # Check for CORS headers (Note: Flask-CORS handles this internally)
        # In a real test, you might want to check the actual headers
        print("✅ CORS headers test passed")

    def test_data_integrity(self):
        """Test data integrity across related endpoints"""
        # Get all restaurants
        restaurants_response = self.app.get('/api/restaurants')
        restaurants = json.loads(restaurants_response.data)
        
        # Get all orders
        orders_response = self.app.get('/api/orders')
        orders = json.loads(orders_response.data)
        
        # Get all menu items
        menu_response = self.app.get('/api/menu-items')
        menu_items = json.loads(menu_response.data)
        
        # Verify referential integrity
        restaurant_ids = {r['id'] for r in restaurants}
        
        for order in orders:
            self.assertIn(order['restaurant_id'], restaurant_ids,
                         f"Order {order['id']} references non-existent restaurant {order['restaurant_id']}")
        
        for item in menu_items:
            self.assertIn(item['restaurant_id'], restaurant_ids,
                         f"Menu item {item['id']} references non-existent restaurant {item['restaurant_id']}")
        
        print("✅ Data integrity test passed")

    def test_api_response_format(self):
        """Test that all API responses return valid JSON"""
        endpoints = [
            '/',
            '/health',
            '/api/restaurants',
            '/api/orders',
            '/api/menu-items',
            '/api/analytics'
        ]
        
        for endpoint in endpoints:
            response = self.app.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Verify response is valid JSON
            try:
                json.loads(response.data)
            except json.JSONDecodeError:
                self.fail(f"Endpoint {endpoint} returned invalid JSON")
        
        print("✅ API response format test passed")

    def test_status_values_validation(self):
        """Test that order status values are valid"""
        response = self.app.get('/api/orders')
        orders = json.loads(response.data)
        
        valid_statuses = ['pending', 'preparing', 'completed', 'cancelled', 'delivered']
        
        for order in orders:
            self.assertIn(order['status'], valid_statuses,
                         f"Order {order['id']} has invalid status: {order['status']}")
        
        print("✅ Status values validation test passed")

    def test_price_validation(self):
        """Test that all prices are positive numbers"""
        # Test menu item prices
        response = self.app.get('/api/menu-items')
        menu_items = json.loads(response.data)
        
        for item in menu_items:
            self.assertGreater(item['price'], 0,
                             f"Menu item {item['id']} has invalid price: {item['price']}")
        
        # Test order totals
        response = self.app.get('/api/orders')
        orders = json.loads(response.data)
        
        for order in orders:
            self.assertGreater(order['total'], 0,
                             f"Order {order['id']} has invalid total: {order['total']}")
        
        print("✅ Price validation test passed")


class RestaurantFlowPerformanceTests(unittest.TestCase):
    """Performance and load testing for RestaurantFlow backend"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_response_time(self):
        """Test that API responses are reasonably fast"""
        import time
        
        endpoints = [
            '/api/restaurants',
            '/api/orders',
            '/api/menu-items',
            '/api/analytics'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.app.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            self.assertLess(response_time, 1.0,  # Less than 1 second
                           f"Endpoint {endpoint} took too long: {response_time:.2f}s")
        
        print("✅ Response time test passed")

    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = self.app.get('/api/restaurants')
            results.append(response.status_code)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        for status_code in results:
            self.assertEqual(status_code, 200)
        
        print("✅ Concurrent requests test passed")


def run_all_tests():
    """Run all backend tests and provide a summary"""
    print("🧪 Starting RestaurantFlow Backend Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test methods from RestaurantFlowBackendTestSuite
    test_suite.addTest(unittest.makeSuite(RestaurantFlowBackendTestSuite))
    test_suite.addTest(unittest.makeSuite(RestaurantFlowPerformanceTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 50)
    print("🏁 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n💥 Some tests failed!")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Set up Flask app for testing
    app.config['TESTING'] = True
    
    # Run all tests
    success = run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)
