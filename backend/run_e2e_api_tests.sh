#!/bin/bash

# E2E API Test Runner for RestaurantFlow_bhatiyani
# Tests actual running backend API (local or remote)

echo "🧪 RestaurantFlow E2E API Test Runner"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_BACKEND_URL="http://localhost:8000"
DEFAULT_TIMEOUT=30

# Parse command line arguments
BACKEND_URL=${1:-$DEFAULT_BACKEND_URL}
TIMEOUT=${2:-$DEFAULT_TIMEOUT}

echo -e "${BLUE}🎯 Target Backend: ${BACKEND_URL}${NC}"
echo -e "${BLUE}⏱️  Timeout: ${TIMEOUT}s${NC}"
echo ""

# Change to backend directory
cd "$(dirname "$0")"

# Check if Python is available
echo -e "${YELLOW}🔍 Checking Python environment...${NC}"
python3 --version
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Python3 is not available${NC}"
    exit 1
fi

# Check if requests library is available
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Installing requests library...${NC}"
    pip3 install requests
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install requests library${NC}"
        exit 1
    fi
fi

# Check if E2E test file exists
if [ ! -f "e2e_api_tests.py" ]; then
    echo -e "${RED}❌ e2e_api_tests.py not found${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🚀 Starting E2E API tests...${NC}"
echo ""

# Run the E2E tests
python3 e2e_api_tests.py --url "$BACKEND_URL" --timeout "$TIMEOUT"

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "====================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 All E2E API tests passed!${NC}"
    echo -e "${GREEN}✅ Backend API at ${BACKEND_URL} is working correctly${NC}"
else
    echo -e "${RED}💥 Some E2E API tests failed!${NC}"
    echo -e "${RED}❌ Check the backend API at ${BACKEND_URL}${NC}"
fi

# Show results file if it exists
if [ -f "e2e_api_test_results.json" ]; then
    echo ""
    echo -e "${BLUE}📄 Results saved to: e2e_api_test_results.json${NC}"
    echo -e "${BLUE}📊 Test Summary:${NC}"
    python3 -c "
import json
try:
    with open('e2e_api_test_results.json', 'r') as f:
        results = json.load(f)
        summary = results.get('summary', {})
        print(f'   ✅ Passed: {summary.get(\"passed\", 0)}')
        print(f'   ❌ Failed: {summary.get(\"failed\", 0)}')
        print(f'   📊 Total: {summary.get(\"total\", 0)}')
        print(f'   🎯 Success Rate: {summary.get(\"success_rate\", 0):.1f}%')
except:
    pass
"
fi

echo ""
echo -e "${BLUE}💡 Usage Examples:${NC}"
echo "   Local backend:  ./run_e2e_api_tests.sh"
echo "   Remote backend: ./run_e2e_api_tests.sh https://your-api-domain.com"
echo "   With timeout:   ./run_e2e_api_tests.sh http://localhost:8000 60"

exit $TEST_EXIT_CODE
