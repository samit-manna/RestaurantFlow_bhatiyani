#!/bin/bash

# E2E Frontend Test Runner for RestaurantFlow_bhatiyani
# Tests actual running frontend application (local or remote)

echo "🧪 RestaurantFlow E2E Frontend Test Runner"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_FRONTEND_URL="http://localhost:3000"
DEFAULT_BACKEND_URL="http://localhost:8000"

# Parse command line arguments
FRONTEND_URL=${1:-$DEFAULT_FRONTEND_URL}
BACKEND_URL=${2:-$DEFAULT_BACKEND_URL}

echo -e "${BLUE}🎯 Target Frontend: ${FRONTEND_URL}${NC}"
echo -e "${BLUE}🔗 Target Backend: ${BACKEND_URL}${NC}"
echo ""

# Change to frontend directory
cd "$(dirname "$0")"

# Check if Node.js is available
echo -e "${YELLOW}🔍 Checking Node.js environment...${NC}"
node --version
npm --version

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Node.js/npm is not available${NC}"
    exit 1
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found${NC}"
    exit 1
fi

# Check testing framework availability
echo -e "${YELLOW}🔍 Checking E2E testing framework...${NC}"

# Check for Cypress
if npm list cypress > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Cypress is available${NC}"
    TEST_FRAMEWORK="cypress"
elif [ -d "cypress" ]; then
    echo -e "${YELLOW}📦 Installing Cypress...${NC}"
    npm install --save-dev cypress
    TEST_FRAMEWORK="cypress"
else
    echo -e "${YELLOW}📦 Installing Cypress for E2E testing...${NC}"
    npm install --save-dev cypress
    TEST_FRAMEWORK="cypress"
fi

# Check for Playwright as alternative
if npm list @playwright/test > /dev/null 2>&1 && [ "$TEST_FRAMEWORK" != "cypress" ]; then
    echo -e "${GREEN}✅ Playwright is available${NC}"
    TEST_FRAMEWORK="playwright"
fi

# If no framework, install Cypress
if [ -z "$TEST_FRAMEWORK" ]; then
    echo -e "${YELLOW}📦 Installing Cypress...${NC}"
    npm install --save-dev cypress
    TEST_FRAMEWORK="cypress"
fi

# Create cypress config if it doesn't exist
if [ "$TEST_FRAMEWORK" = "cypress" ] && [ ! -f "cypress.config.js" ]; then
    echo -e "${YELLOW}⚙️ Creating Cypress configuration...${NC}"
    cat > cypress.config.js << EOF
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: '${FRONTEND_URL}',
    supportFile: false,
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    env: {
      FRONTEND_URL: '${FRONTEND_URL}',
      BACKEND_URL: '${BACKEND_URL}'
    }
  }
})
EOF
fi

echo ""
echo -e "${YELLOW}🚀 Starting E2E frontend tests...${NC}"
echo ""

# Check if frontend is accessible
echo -e "${YELLOW}🔍 Checking frontend accessibility...${NC}"
curl -s --connect-timeout 5 "$FRONTEND_URL" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend is accessible at ${FRONTEND_URL}${NC}"
else
    echo -e "${YELLOW}⚠️ Frontend may not be accessible at ${FRONTEND_URL}${NC}"
    echo -e "${YELLOW}   Tests will still run but may fail${NC}"
fi

# Check if backend is accessible
echo -e "${YELLOW}🔍 Checking backend accessibility...${NC}"
curl -s --connect-timeout 5 "${BACKEND_URL}/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend is accessible at ${BACKEND_URL}${NC}"
else
    echo -e "${YELLOW}⚠️ Backend may not be accessible at ${BACKEND_URL}${NC}"
    echo -e "${YELLOW}   Some integration tests may fail${NC}"
fi

echo ""

# Run tests based on available framework
if [ "$TEST_FRAMEWORK" = "cypress" ]; then
    echo -e "${BLUE}🧪 Running Cypress E2E tests...${NC}"
    
    # Check if test file exists
    if [ ! -f "cypress/e2e/restaurantflow.cy.js" ]; then
        echo -e "${RED}❌ Cypress test file not found: cypress/e2e/restaurantflow.cy.js${NC}"
        exit 1
    fi
    
    # Set environment variables for Cypress
    export CYPRESS_FRONTEND_URL="$FRONTEND_URL"
    export CYPRESS_BACKEND_URL="$BACKEND_URL"
    
    # Run Cypress tests
    npx cypress run --spec "cypress/e2e/restaurantflow.cy.js" --env FRONTEND_URL="$FRONTEND_URL",BACKEND_URL="$BACKEND_URL"
    TEST_EXIT_CODE=$?
    
elif [ "$TEST_FRAMEWORK" = "playwright" ]; then
    echo -e "${BLUE}🧪 Running Playwright E2E tests...${NC}"
    
    # Set environment variables for Playwright
    export FRONTEND_URL="$FRONTEND_URL"
    export BACKEND_URL="$BACKEND_URL"
    
    # Run Playwright tests
    npx playwright test e2e/restaurantflow.e2e.spec.ts
    TEST_EXIT_CODE=$?
    
else
    echo -e "${RED}❌ No suitable E2E testing framework found${NC}"
    exit 1
fi

echo ""
echo "=========================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 All E2E frontend tests passed!${NC}"
    echo -e "${GREEN}✅ Frontend at ${FRONTEND_URL} is working correctly${NC}"
else
    echo -e "${RED}💥 Some E2E frontend tests failed!${NC}"
    echo -e "${RED}❌ Check the frontend application at ${FRONTEND_URL}${NC}"
fi

# Show test artifacts
echo ""
echo -e "${BLUE}📁 Test Artifacts:${NC}"
if [ -d "cypress/screenshots" ]; then
    SCREENSHOT_COUNT=$(find cypress/screenshots -name "*.png" 2>/dev/null | wc -l)
    echo "   📸 Screenshots: $SCREENSHOT_COUNT files in cypress/screenshots/"
fi

if [ -d "cypress/videos" ]; then
    VIDEO_COUNT=$(find cypress/videos -name "*.mp4" 2>/dev/null | wc -l)
    echo "   🎥 Videos: $VIDEO_COUNT files in cypress/videos/"
fi

echo ""
echo -e "${BLUE}💡 Usage Examples:${NC}"
echo "   Local frontend:  ./run_e2e_frontend_tests.sh"
echo "   Remote frontend: ./run_e2e_frontend_tests.sh https://your-app-domain.com"
echo "   With backend:    ./run_e2e_frontend_tests.sh http://localhost:3000 http://localhost:8000"
echo ""
echo -e "${BLUE}🔧 Manual Cypress UI:${NC}"
echo "   npx cypress open"

exit $TEST_EXIT_CODE
