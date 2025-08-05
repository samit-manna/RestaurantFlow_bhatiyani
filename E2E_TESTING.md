# 🧪 RestaurantFlow E2E Testing Guide

This guide covers End-to-End (E2E) testing for RestaurantFlow_bhatiyani, testing the actual running application rather than isolated components.

## 📁 E2E Test Files Overview

### Backend API E2E Tests
- **File**: `backend/e2e_api_tests.py`
- **Runner**: `backend/run_e2e_api_tests.sh`
- **Purpose**: Tests actual running backend API endpoints
- **Framework**: Python requests library

### Frontend E2E Tests
- **File**: `frontend/cypress/e2e/restaurantflow.cy.js`
- **Runner**: `frontend/run_e2e_frontend_tests.sh`
- **Purpose**: Tests actual running frontend application
- **Framework**: Cypress

## 🚀 Quick Start

### Prerequisites
- **Backend running** at `http://localhost:8000` (or custom URL)
- **Frontend running** at `http://localhost:3000` (or custom URL)
- Python 3.7+ for API tests
- Node.js 14+ for frontend tests

### Running E2E Tests

```bash
# Test backend API (local)
cd backend
./run_e2e_api_tests.sh

# Test frontend (local)
cd frontend
./run_e2e_frontend_tests.sh

# Test against remote servers
./run_e2e_api_tests.sh https://your-api.herokuapp.com
./run_e2e_frontend_tests.sh https://your-app.vercel.app https://your-api.herokuapp.com
```

## 🔧 Backend API E2E Tests

### What It Tests
- ✅ **API Health** - Server availability and health endpoints
- ✅ **Restaurants API** - CRUD operations and data validation
- ✅ **Orders API** - Order management and status handling
- ✅ **Menu Items API** - Menu data and restaurant relationships
- ✅ **Analytics API** - Dashboard metrics and analytics data
- ✅ **Data Consistency** - Cross-endpoint data integrity
- ✅ **Performance** - Response times and concurrent requests

### Running API Tests

```bash
# Local backend
cd backend
./run_e2e_api_tests.sh

# Remote backend
./run_e2e_api_tests.sh https://restaurant-flow-bhatiyani.railway.app

# With custom timeout
./run_e2e_api_tests.sh http://localhost:8000 60

# Direct Python execution
python3 e2e_api_tests.py --url http://localhost:8000 --timeout 30
```

### API Test Output Example
```
🚀 Starting E2E API Tests for: http://localhost:8000
============================================================

🏥 Testing API Health...
✅ PASS Root endpoint (0.05s)
✅ PASS Health endpoint (0.03s)

🏪 Testing Restaurants API...
✅ PASS Get all restaurants (0.12s) - Found 3 restaurants
✅ PASS Get single restaurant (0.08s) - Retrieved restaurant 1
✅ PASS Get non-existent restaurant (0.06s) - Correctly returned 404

📋 Testing Orders API...
✅ PASS Get all orders (0.10s) - Found 3 orders
✅ PASS Get single order (0.07s) - Retrieved order 1

🎉 All 15 tests passed! API is working correctly.
```

## 🎨 Frontend E2E Tests

### What It Tests
- ✅ **Application Loading** - Page loads and navigation visibility
- ✅ **Navigation** - Page routing and menu functionality
- ✅ **Data Loading** - API integration and data display
- ✅ **Search & Filtering** - User interaction features
- ✅ **Responsive Design** - Mobile, tablet, and desktop layouts
- ✅ **Performance** - Load times and error handling
- ✅ **Accessibility** - Keyboard navigation and semantic HTML
- ✅ **Backend Integration** - Frontend-API communication

### Running Frontend Tests

```bash
# Local frontend (assumes backend at localhost:8000)
cd frontend
./run_e2e_frontend_tests.sh

# Remote frontend with remote backend
./run_e2e_frontend_tests.sh https://restaurant-flow-bhatiyani.vercel.app https://restaurant-flow-bhatiyani.railway.app

# Custom URLs
./run_e2e_frontend_tests.sh http://localhost:3000 http://localhost:8000

# Manual Cypress UI (for debugging)
npx cypress open
```

### Frontend Test Output Example
```
🧪 RestaurantFlow E2E Frontend Test Runner
==========================================
🎯 Target Frontend: http://localhost:3000
🔗 Target Backend: http://localhost:8000

✅ Frontend is accessible at http://localhost:3000
✅ Backend is accessible at http://localhost:8000

🧪 Running Cypress E2E tests...

  🧪 RestaurantFlow E2E Tests
    🏠 Application Loading
      ✓ should load the main application (1250ms)
      ✓ should display navigation menu (890ms)
      ✓ should handle page refresh (1100ms)
    
    🧭 Navigation
      ✓ should navigate to Dashboard (920ms)
      ✓ should navigate to Restaurants (1050ms)
      ✓ should navigate to Orders (980ms)
      ✓ should navigate to Analytics (1120ms)

🎉 All E2E frontend tests passed!
```

## 📊 Test Scenarios

### Backend API Test Scenarios

#### Health Check Tests
```python
# Tests API availability
GET / → 200 OK with API info
GET /health → 200 OK with healthy status
```

#### Restaurant Management Tests
```python
# CRUD operations
GET /api/restaurants → List all restaurants
GET /api/restaurants/1 → Get specific restaurant
GET /api/restaurants/999 → 404 Not Found

# Data validation
Verify restaurant structure (id, name, address, phone)
Check referential integrity with orders/menu items
```

#### Order Management Tests
```python
# Order operations
GET /api/orders → List all orders
GET /api/orders/1 → Get specific order
GET /api/orders/999 → 404 Not Found

# Status validation
Verify valid order statuses (pending, preparing, completed)
Check price validation (positive numbers)
```

### Frontend E2E Test Scenarios

#### Navigation Flow Tests
```javascript
// Page navigation
Visit homepage → Check navigation visible
Click "Restaurants" → Verify restaurants page loads
Click "Orders" → Verify orders page loads
Click "Dashboard" → Verify dashboard loads
```

#### Data Integration Tests
```javascript
// API data display
Navigate to Restaurants → Wait for data → Verify restaurant names visible
Navigate to Orders → Wait for data → Verify customer names visible
Navigate to Dashboard → Wait for data → Verify metrics displayed
```

#### User Interaction Tests
```javascript
// Search functionality
Go to Restaurants → Type in search box → Verify filtered results
Go to Orders → Select status filter → Verify filtered orders
```

## 🔧 Configuration

### Backend API Test Configuration
```python
# Environment variables
BACKEND_URL = "http://localhost:8000"  # Target API URL
TIMEOUT = 30  # Request timeout in seconds

# Test settings
REQUEST_TIMEOUT = 30
MAX_RESPONSE_TIME = 2.0  # Performance threshold
CONCURRENT_REQUESTS = 10  # Load testing
```

### Frontend Test Configuration
```javascript
// Cypress configuration (cypress.config.js)
module.exports = {
  e2e: {
    baseUrl: 'http://localhost:3000',
    env: {
      FRONTEND_URL: 'http://localhost:3000',
      BACKEND_URL: 'http://localhost:8000'
    },
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000
  }
}
```

## 🐛 Troubleshooting

### Common Backend API Issues

#### Connection Errors
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check specific port
netstat -an | grep 8000

# Start backend if not running
cd backend
python3 main.py
```

#### API Response Issues
```bash
# Test specific endpoints
curl -v http://localhost:8000/api/restaurants
curl -v http://localhost:8000/api/orders

# Check CORS headers
curl -H "Origin: http://localhost:3000" -v http://localhost:8000/api/restaurants
```

### Common Frontend Issues

#### Application Not Loading
```bash
# Check if frontend is running
curl http://localhost:3000

# Start frontend if not running
cd frontend
npm start
```

#### Cypress Issues
```bash
# Clear Cypress cache
npx cypress cache clear

# Install Cypress
npm install --save-dev cypress

# Verify Cypress installation
npx cypress verify
```

#### Test Failures
```bash
# Run with debug output
DEBUG=cypress:* npx cypress run

# Open Cypress UI for debugging
npx cypress open

# Check console logs in browser
```

## 📈 Performance Benchmarks

### API Performance Targets
- **Response Time**: < 200ms for GET requests
- **Error Rate**: < 1% for all endpoints
- **Concurrent Users**: Handle 10+ simultaneous requests
- **Availability**: 99.9% uptime

### Frontend Performance Targets
- **Page Load**: < 3 seconds first load
- **Navigation**: < 1 second between pages
- **API Data**: < 2 seconds to display data
- **Search**: < 500ms to filter results

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  api-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Start Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python main.py &
          sleep 10
      
      - name: Run API E2E Tests
        run: |
          cd backend
          ./run_e2e_api_tests.sh

  frontend-e2e:
    runs-on: ubuntu-latest
    needs: api-e2e
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      
      - name: Start Frontend
        run: |
          cd frontend
          npm install
          npm start &
          sleep 15
      
      - name: Run Frontend E2E Tests
        run: |
          cd frontend
          ./run_e2e_frontend_tests.sh
```

## 📝 Test Maintenance

### Adding New API Tests
1. Add test method to `RestaurantFlowE2EAPITester` class
2. Include in `run_all_tests()` method
3. Update documentation

### Adding New Frontend Tests
1. Add test case to appropriate `describe` block
2. Follow existing test patterns
3. Use proper selectors and waits

### Best Practices
- ✅ Test against real running applications
- ✅ Use proper waits instead of fixed delays
- ✅ Test both success and error scenarios
- ✅ Include performance assertions
- ✅ Test on multiple viewports
- ✅ Verify accessibility features
- ✅ Test API integration thoroughly
- ✅ Clean up test data when needed

---

**Last Updated**: August 2025  
**Version**: 1.0.0  
**Framework**: Python + Cypress  
**Maintained By**: RestaurantFlow_bhatiyani Team
