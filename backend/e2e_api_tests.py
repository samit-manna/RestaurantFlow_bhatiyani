#!/usr/bin/env python3
"""
End-to-End API Tests for RestaurantFlow_bhatiyani
Tests actual running backend API (local or remote)
"""

import requests
import json
import time
import sys
import argparse
from typing import Dict, Any, List
from urllib.parse import urljoin

class RestaurantFlowE2EAPITester:
    """End-to-End API testing for RestaurantFlow backend"""
    
    def __init__(self, base_url: str):
        """Initialize with base URL (local or remote)"""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'RestaurantFlow-E2E-Tester/1.0'
        })
        
        # Test results tracking
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = "", response_time: float = 0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        time_info = f"({response_time:.2f}s)" if response_time > 0 else ""
        
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'response_time': response_time
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
            print(f"{status} {test_name} {time_info}")
        else:
            self.failed_tests += 1
            print(f"{status} {test_name} {time_info}")
            if message:
                print(f"    └─ {message}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> tuple:
        """Make HTTP request and return response with timing"""
        url = urljoin(self.base_url, endpoint)
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            end_time = time.time()
            response_time = end_time - start_time
            return response, response_time, None
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time = end_time - start_time
            return None, response_time, str(e)
    
    def test_health_check(self):
        """Test if the API is running and healthy"""
        print("\n🏥 Testing API Health...")
        
        # Test root endpoint
        response, response_time, error = self.make_request('GET', '/')
        if error:
            self.log_test("Root endpoint connectivity", False, f"Connection error: {error}", response_time)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'message' in data and 'RestaurantFlow' in data['message']:
                    self.log_test("Root endpoint", True, "", response_time)
                else:
                    self.log_test("Root endpoint", False, "Invalid response format", response_time)
            except json.JSONDecodeError:
                self.log_test("Root endpoint", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Root endpoint", False, f"HTTP {response.status_code}", response_time)
        
        # Test health endpoint
        response, response_time, error = self.make_request('GET', '/health')
        if error:
            self.log_test("Health endpoint", False, f"Connection error: {error}", response_time)
            return False
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Health endpoint", True, "", response_time)
                    return True
                else:
                    self.log_test("Health endpoint", False, "Service not healthy", response_time)
            except json.JSONDecodeError:
                self.log_test("Health endpoint", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Health endpoint", False, f"HTTP {response.status_code}", response_time)
        
        return False
    
    def test_restaurants_api(self):
        """Test restaurants API endpoints"""
        print("\n🏪 Testing Restaurants API...")
        
        # Test GET all restaurants
        response, response_time, error = self.make_request('GET', '/api/restaurants')
        if error:
            self.log_test("Get all restaurants", False, f"Connection error: {error}", response_time)
            return
        
        if response.status_code == 200:
            try:
                restaurants = response.json()
                if isinstance(restaurants, list) and len(restaurants) > 0:
                    self.log_test("Get all restaurants", True, f"Found {len(restaurants)} restaurants", response_time)
                    
                    # Test GET single restaurant with first restaurant ID
                    restaurant_id = restaurants[0]['id']
                    response, response_time, error = self.make_request('GET', f'/api/restaurants/{restaurant_id}')
                    
                    if response and response.status_code == 200:
                        restaurant = response.json()
                        if restaurant.get('id') == restaurant_id:
                            self.log_test("Get single restaurant", True, f"Retrieved restaurant {restaurant_id}", response_time)
                        else:
                            self.log_test("Get single restaurant", False, "ID mismatch", response_time)
                    else:
                        self.log_test("Get single restaurant", False, f"HTTP {response.status_code if response else 'Connection error'}", response_time)
                    
                    # Test non-existent restaurant
                    response, response_time, error = self.make_request('GET', '/api/restaurants/99999')
                    if response and response.status_code == 404:
                        self.log_test("Get non-existent restaurant", True, "Correctly returned 404", response_time)
                    else:
                        self.log_test("Get non-existent restaurant", False, f"Expected 404, got {response.status_code if response else 'Connection error'}", response_time)
                
                else:
                    self.log_test("Get all restaurants", False, "Empty or invalid response", response_time)
            except json.JSONDecodeError:
                self.log_test("Get all restaurants", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Get all restaurants", False, f"HTTP {response.status_code}", response_time)
    
    def test_orders_api(self):
        """Test orders API endpoints"""
        print("\n📋 Testing Orders API...")
        
        # Test GET all orders
        response, response_time, error = self.make_request('GET', '/api/orders')
        if error:
            self.log_test("Get all orders", False, f"Connection error: {error}", response_time)
            return
        
        if response.status_code == 200:
            try:
                orders = response.json()
                if isinstance(orders, list):
                    self.log_test("Get all orders", True, f"Found {len(orders)} orders", response_time)
                    
                    if len(orders) > 0:
                        # Test GET single order
                        order_id = orders[0]['id']
                        response, response_time, error = self.make_request('GET', f'/api/orders/{order_id}')
                        
                        if response and response.status_code == 200:
                            order = response.json()
                            if order.get('id') == order_id:
                                self.log_test("Get single order", True, f"Retrieved order {order_id}", response_time)
                            else:
                                self.log_test("Get single order", False, "ID mismatch", response_time)
                        else:
                            self.log_test("Get single order", False, f"HTTP {response.status_code if response else 'Connection error'}", response_time)
                    
                    # Test non-existent order
                    response, response_time, error = self.make_request('GET', '/api/orders/99999')
                    if response and response.status_code == 404:
                        self.log_test("Get non-existent order", True, "Correctly returned 404", response_time)
                    else:
                        self.log_test("Get non-existent order", False, f"Expected 404, got {response.status_code if response else 'Connection error'}", response_time)
                
                else:
                    self.log_test("Get all orders", False, "Invalid response format", response_time)
            except json.JSONDecodeError:
                self.log_test("Get all orders", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Get all orders", False, f"HTTP {response.status_code}", response_time)
    
    def test_menu_items_api(self):
        """Test menu items API endpoints"""
        print("\n🍽️ Testing Menu Items API...")
        
        # Test GET all menu items
        response, response_time, error = self.make_request('GET', '/api/menu-items')
        if error:
            self.log_test("Get all menu items", False, f"Connection error: {error}", response_time)
            return
        
        if response.status_code == 200:
            try:
                menu_items = response.json()
                if isinstance(menu_items, list):
                    self.log_test("Get all menu items", True, f"Found {len(menu_items)} menu items", response_time)
                    
                    if len(menu_items) > 0:
                        # Test GET menu items for specific restaurant
                        restaurant_id = menu_items[0]['restaurant_id']
                        response, response_time, error = self.make_request('GET', f'/api/menu-items/{restaurant_id}')
                        
                        if response and response.status_code == 200:
                            restaurant_menu = response.json()
                            if isinstance(restaurant_menu, list):
                                # Verify all items belong to the restaurant
                                valid_menu = all(item.get('restaurant_id') == restaurant_id for item in restaurant_menu)
                                if valid_menu:
                                    self.log_test("Get restaurant menu", True, f"Found {len(restaurant_menu)} items for restaurant {restaurant_id}", response_time)
                                else:
                                    self.log_test("Get restaurant menu", False, "Menu items don't match restaurant ID", response_time)
                            else:
                                self.log_test("Get restaurant menu", False, "Invalid response format", response_time)
                        else:
                            self.log_test("Get restaurant menu", False, f"HTTP {response.status_code if response else 'Connection error'}", response_time)
                
                else:
                    self.log_test("Get all menu items", False, "Invalid response format", response_time)
            except json.JSONDecodeError:
                self.log_test("Get all menu items", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Get all menu items", False, f"HTTP {response.status_code}", response_time)
    
    def test_analytics_api(self):
        """Test analytics API endpoints"""
        print("\n📊 Testing Analytics API...")
        
        # Test GET analytics
        response, response_time, error = self.make_request('GET', '/api/analytics')
        if error:
            self.log_test("Get analytics", False, f"Connection error: {error}", response_time)
            return
        
        if response.status_code == 200:
            try:
                analytics = response.json()
                required_keys = ['daily_orders', 'popular_items']
                
                if all(key in analytics for key in required_keys):
                    self.log_test("Get analytics", True, "Analytics data structure is valid", response_time)
                    
                    # Test dashboard data for restaurant 1
                    response, response_time, error = self.make_request('GET', '/api/analytics/dashboard/1')
                    if response and response.status_code == 200:
                        dashboard = response.json()
                        dashboard_keys = ['today_orders', 'pending_orders', 'today_revenue', 'active_menu_items']
                        
                        if all(key in dashboard for key in dashboard_keys):
                            self.log_test("Get dashboard data", True, "Dashboard data structure is valid", response_time)
                        else:
                            self.log_test("Get dashboard data", False, "Missing dashboard fields", response_time)
                    else:
                        self.log_test("Get dashboard data", False, f"HTTP {response.status_code if response else 'Connection error'}", response_time)
                
                else:
                    self.log_test("Get analytics", False, "Missing required analytics fields", response_time)
            except json.JSONDecodeError:
                self.log_test("Get analytics", False, "Invalid JSON response", response_time)
        else:
            self.log_test("Get analytics", False, f"HTTP {response.status_code}", response_time)
    
    def test_data_consistency(self):
        """Test data consistency across endpoints"""
        print("\n🔗 Testing Data Consistency...")
        
        try:
            # Get all data
            restaurants_resp, _, _ = self.make_request('GET', '/api/restaurants')
            orders_resp, _, _ = self.make_request('GET', '/api/orders')
            menu_resp, _, _ = self.make_request('GET', '/api/menu-items')
            
            if all(resp and resp.status_code == 200 for resp in [restaurants_resp, orders_resp, menu_resp]):
                restaurants = restaurants_resp.json()
                orders = orders_resp.json()
                menu_items = menu_resp.json()
                
                restaurant_ids = {r['id'] for r in restaurants}
                
                # Check order consistency
                invalid_order_restaurants = [o for o in orders if o.get('restaurant_id') not in restaurant_ids]
                if not invalid_order_restaurants:
                    self.log_test("Order-Restaurant consistency", True, f"All {len(orders)} orders reference valid restaurants")
                else:
                    self.log_test("Order-Restaurant consistency", False, f"{len(invalid_order_restaurants)} orders reference invalid restaurants")
                
                # Check menu item consistency
                invalid_menu_restaurants = [m for m in menu_items if m.get('restaurant_id') not in restaurant_ids]
                if not invalid_menu_restaurants:
                    self.log_test("Menu-Restaurant consistency", True, f"All {len(menu_items)} menu items reference valid restaurants")
                else:
                    self.log_test("Menu-Restaurant consistency", False, f"{len(invalid_menu_restaurants)} menu items reference invalid restaurants")
            
            else:
                self.log_test("Data consistency", False, "Could not retrieve all required data")
        
        except Exception as e:
            self.log_test("Data consistency", False, f"Error during consistency check: {str(e)}")
    
    def test_performance(self):
        """Test API performance"""
        print("\n⚡ Testing API Performance...")
        
        endpoints = [
            '/api/restaurants',
            '/api/orders',
            '/api/menu-items',
            '/api/analytics'
        ]
        
        for endpoint in endpoints:
            response, response_time, error = self.make_request('GET', endpoint)
            
            if error:
                self.log_test(f"Performance {endpoint}", False, f"Connection error: {error}", response_time)
                continue
            
            if response and response.status_code == 200:
                if response_time < 2.0:  # Less than 2 seconds
                    self.log_test(f"Performance {endpoint}", True, f"Response time acceptable", response_time)
                else:
                    self.log_test(f"Performance {endpoint}", False, f"Response time too slow", response_time)
            else:
                self.log_test(f"Performance {endpoint}", False, f"HTTP {response.status_code if response else 'No response'}", response_time)
    
    def run_all_tests(self):
        """Run complete E2E test suite"""
        print(f"🚀 Starting E2E API Tests for: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test API health first
        if not self.test_health_check():
            print(f"\n❌ API is not healthy or accessible at {self.base_url}")
            print("Please ensure the backend server is running and accessible.")
            return False
        
        # Run all test categories
        self.test_restaurants_api()
        self.test_orders_api()
        self.test_menu_items_api()
        self.test_analytics_api()
        self.test_data_consistency()
        self.test_performance()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 E2E API Test Summary:")
        print(f"   ✅ Passed: {self.passed_tests}")
        print(f"   ❌ Failed: {self.failed_tests}")
        print(f"   📊 Total: {self.passed_tests + self.failed_tests}")
        print(f"   ⏱️  Duration: {total_time:.2f}s")
        print(f"   🎯 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n❌ {self.failed_tests} tests failed. Check the API implementation or server status.")
            return False
        else:
            print(f"\n🎉 All {self.passed_tests} tests passed! API is working correctly.")
            return True


def main():
    """Main function with CLI arguments"""
    parser = argparse.ArgumentParser(description='RestaurantFlow E2E API Tester')
    parser.add_argument('--url', '-u', 
                       default='http://localhost:8000',
                       help='Backend API URL (default: http://localhost:8000)')
    parser.add_argument('--timeout', '-t',
                       type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    
    args = parser.parse_args()
    
    print(f"🧪 RestaurantFlow E2E API Tester")
    print(f"Target: {args.url}")
    print(f"Timeout: {args.timeout}s")
    
    # Create and run tester
    tester = RestaurantFlowE2EAPITester(args.url)
    tester.session.timeout = args.timeout
    
    success = tester.run_all_tests()
    
    # Export results to JSON if needed
    results_file = 'e2e_api_test_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'target_url': args.url,
            'timestamp': time.time(),
            'summary': {
                'passed': tester.passed_tests,
                'failed': tester.failed_tests,
                'total': tester.passed_tests + tester.failed_tests,
                'success_rate': (tester.passed_tests / (tester.passed_tests + tester.failed_tests) * 100) if (tester.passed_tests + tester.failed_tests) > 0 else 0
            },
            'test_results': tester.test_results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
