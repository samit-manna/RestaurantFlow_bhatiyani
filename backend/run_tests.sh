#!/bin/bash

# Backend Test Runner for RestaurantFlow_bhatiyani
# This script runs all backend tests and provides a comprehensive report

echo "🧪 RestaurantFlow Backend Test Runner"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to backend directory
cd "$(dirname "$0")"

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"
echo ""

# Check if Flask is available
echo -e "${YELLOW}🔍 Checking Python environment...${NC}"
python3 --version
pip3 show flask > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Flask is installed${NC}"
else
    echo -e "${RED}❌ Flask is not installed. Installing...${NC}"
    pip3 install flask flask-cors
fi

# Check if test file exists
if [ ! -f "test_backend.py" ]; then
    echo -e "${RED}❌ test_backend.py not found${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🚀 Starting backend tests...${NC}"
echo ""

# Run the tests
python3 test_backend.py

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "====================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 All backend tests passed!${NC}"
else
    echo -e "${RED}💥 Some backend tests failed!${NC}"
fi

# Additional checks
echo ""
echo -e "${YELLOW}🔍 Running additional checks...${NC}"

# Check if main.py can be imported
python3 -c "import main; print('✅ main.py imports successfully')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ main.py has import issues${NC}"
fi

# Check for syntax errors
python3 -m py_compile main.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ main.py syntax is valid${NC}"
else
    echo -e "${RED}❌ main.py has syntax errors${NC}"
fi

# Test if server can start (quick test)
echo -e "${YELLOW}🔍 Testing server startup...${NC}"
timeout 5 python3 -c "
import main
app = main.app
with app.test_client() as client:
    response = client.get('/')
    if response.status_code == 200:
        print('✅ Server starts successfully')
    else:
        print('❌ Server startup failed')
" 2>/dev/null

echo ""
echo -e "${BLUE}📊 Test Summary Complete${NC}"
exit $TEST_EXIT_CODE
