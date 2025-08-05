#!/bin/bash

# Frontend Test Runner for RestaurantFlow_bhatiyani
# This script runs all frontend tests and provides a comprehensive report

echo "🧪 RestaurantFlow Frontend Test Runner"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to frontend directory
cd "$(dirname "$0")"

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"
echo ""

# Check if Node.js and npm are available
echo -e "${YELLOW}🔍 Checking Node.js environment...${NC}"
node --version
npm --version

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found${NC}"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
fi

# Check if test dependencies are installed
echo -e "${YELLOW}🔍 Checking test dependencies...${NC}"

# Install testing dependencies if not present
npm list @testing-library/react > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Installing @testing-library/react...${NC}"
    npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
fi

npm list jest > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Installing jest...${NC}"
    npm install --save-dev jest
fi

echo ""
echo -e "${YELLOW}🚀 Starting frontend tests...${NC}"
echo ""

# Check if test files exist
TEST_FILES_FOUND=false

if [ -f "src/__tests__/comprehensive_frontend_tests.test.tsx" ]; then
    echo -e "${GREEN}✅ Found comprehensive frontend tests${NC}"
    TEST_FILES_FOUND=true
fi

if [ -f "src/App.test.tsx" ]; then
    echo -e "${GREEN}✅ Found App.test.tsx${NC}"
    TEST_FILES_FOUND=true
fi

if [ "$TEST_FILES_FOUND" = false ]; then
    echo -e "${RED}❌ No test files found${NC}"
    exit 1
fi

# Run the tests
echo -e "${BLUE}🧪 Running Jest tests...${NC}"
npm test -- --watchAll=false --coverage=false --verbose

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "======================================"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 All frontend tests passed!${NC}"
else
    echo -e "${RED}💥 Some frontend tests failed or encountered issues!${NC}"
fi

# Additional checks
echo ""
echo -e "${YELLOW}🔍 Running additional checks...${NC}"

# Check TypeScript compilation
echo -e "${YELLOW}📝 Checking TypeScript compilation...${NC}"
npx tsc --noEmit > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ TypeScript compilation successful${NC}"
else
    echo -e "${YELLOW}⚠️  TypeScript compilation has warnings${NC}"
fi

# Check if build works
echo -e "${YELLOW}🏗️  Testing build process...${NC}"
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build process successful${NC}"
else
    echo -e "${RED}❌ Build process failed${NC}"
fi

# Lint check if available
if npm list eslint > /dev/null 2>&1; then
    echo -e "${YELLOW}🔍 Running ESLint...${NC}"
    npx eslint src --ext .tsx,.ts --max-warnings 10 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ESLint passed${NC}"
    else
        echo -e "${YELLOW}⚠️  ESLint found some issues${NC}"
    fi
fi

# Check bundle size if build exists
if [ -d "build" ]; then
    echo -e "${YELLOW}📊 Checking bundle size...${NC}"
    BUILD_SIZE=$(du -sh build | cut -f1)
    echo -e "${BLUE}📦 Build size: $BUILD_SIZE${NC}"
fi

echo ""
echo -e "${BLUE}📊 Test Summary Complete${NC}"

# Print test file locations
echo ""
echo -e "${BLUE}📁 Test Files Location:${NC}"
echo "   - Backend tests: backend/test_backend.py"
echo "   - Frontend tests: frontend/src/__tests__/comprehensive_frontend_tests.test.tsx"
echo "   - Test runners: backend/run_tests.sh, frontend/run_tests.sh"

exit $TEST_EXIT_CODE
