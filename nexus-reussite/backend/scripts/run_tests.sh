#!/bin/bash

# Comprehensive Test Runner for Nexus Réussite Backend
# This script runs all testing stages: unit, integration, mutation, load, and security tests

set -e  # Exit on any error

echo "🚀 Starting Comprehensive Test Suite for Nexus Réussite Backend"
echo "================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create necessary directories
print_status "Creating output directories..."
mkdir -p reports htmlcov logs

# Step 1: Setup Environment
print_status "Setting up test environment..."
export TESTING=True
export SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
export SECRET_KEY=test-secret-key
export JWT_SECRET_KEY=test-jwt-secret
export OPENAI_API_KEY=test-openai-key
export FLASK_ENV=testing

# Step 2: Run Unit Tests with Coverage
print_status "Running unit tests with coverage analysis..."
if pytest tests/unit/ --cov=src --cov-report=html:htmlcov --cov-report=xml:coverage.xml --cov-report=term-missing --cov-fail-under=90 --junitxml=reports/junit.xml -v; then
    print_success "Unit tests completed successfully"
    UNIT_TESTS_PASSED=true
else
    print_error "Unit tests failed"
    UNIT_TESTS_PASSED=false
fi

# Step 3: Run Integration Tests
print_status "Running integration tests..."
if pytest tests/integration/ -v --tb=short; then
    print_success "Integration tests completed successfully"
    INTEGRATION_TESTS_PASSED=true
else
    print_error "Integration tests failed"
    INTEGRATION_TESTS_PASSED=false
fi

# Step 4: Run Mutation Testing (if unit tests passed)
if [ "$UNIT_TESTS_PASSED" = true ]; then
    print_status "Running mutation testing..."

    # Check if mutmut is installed
    if ! command -v mutmut &> /dev/null; then
        print_warning "mutmut not found, installing..."
        pip install mutmut
    fi

    # Run mutation testing
    if mutmut run --paths-to-mutate src/services/,src/models/,src/utils/ --runner "python -m pytest tests/unit/ -x --tb=no -q" --timeout 120; then
        mutmut html-report
        MUTATION_SCORE=$(mutmut results | grep "Mutation score" | awk '{print $3}' | tr -d '%')
        if [ "${MUTATION_SCORE%.*}" -ge 90 ]; then
            print_success "Mutation testing passed with score: ${MUTATION_SCORE}%"
            MUTATION_TESTS_PASSED=true
        else
            print_warning "Mutation testing score below 90%: ${MUTATION_SCORE}%"
            MUTATION_TESTS_PASSED=false
        fi
    else
        print_error "Mutation testing failed"
        MUTATION_TESTS_PASSED=false
    fi
else
    print_warning "Skipping mutation testing due to unit test failures"
    MUTATION_TESTS_PASSED=false
fi

# Step 5: Run Performance/Load Tests
print_status "Running performance tests..."

# Check if the application is running
if ! curl -f http://localhost:5000/health > /dev/null 2>&1; then
    print_warning "Application not running, starting test server..."
    python src/main_production.py &
    APP_PID=$!
    sleep 5

    # Wait for server to be ready
    for i in {1..30}; do
        if curl -f http://localhost:5000/health > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
fi

# Run smoke tests
print_status "Running smoke tests..."
if locust -f tests/performance/locustfile.py --headless -u 10 -r 2 --run-time 30s --host=http://localhost:5000 --html reports/smoke_test_report.html; then
    print_success "Smoke tests completed successfully"
    SMOKE_TESTS_PASSED=true
else
    print_error "Smoke tests failed"
    SMOKE_TESTS_PASSED=false
fi

# Run load tests
print_status "Running load tests..."
if locust -f tests/performance/locustfile.py --headless -u 50 -r 5 --run-time 2m --host=http://localhost:5000 --html reports/load_test_report.html; then
    print_success "Load tests completed successfully"
    LOAD_TESTS_PASSED=true
else
    print_error "Load tests failed"
    LOAD_TESTS_PASSED=false
fi

# Step 6: Run Security Tests
print_status "Running security tests..."

# Check if OWASP ZAP is available
if command -v zap-cli &> /dev/null || [ -f "/usr/share/zaproxy/zap.sh" ]; then
    print_status "Starting OWASP ZAP daemon..."

    # Start ZAP in daemon mode
    if command -v zap-cli &> /dev/null; then
        zap-cli start --start-options '-daemon -config api.disablekey=true -port 8080' &
    else
        /usr/share/zaproxy/zap.sh -daemon -config api.disablekey=true -port 8080 &
    fi

    ZAP_PID=$!
    sleep 10  # Give ZAP time to start

    # Run security tests
    if pytest tests/security/ -v --tb=short; then
        print_success "Security tests completed successfully"
        SECURITY_TESTS_PASSED=true
    else
        print_error "Security tests failed"
        SECURITY_TESTS_PASSED=false
    fi

    # Stop ZAP
    kill $ZAP_PID 2>/dev/null || true
else
    print_warning "OWASP ZAP not found, skipping security tests"
    print_warning "Install ZAP to run security tests: https://www.zaproxy.org/download/"
    SECURITY_TESTS_PASSED=false
fi

# Cleanup
if [ ! -z "$APP_PID" ]; then
    kill $APP_PID 2>/dev/null || true
fi

# Generate comprehensive report
print_status "Generating test report..."
cat > reports/test_summary.txt << EOF
Nexus Réussite Backend - Test Execution Summary
===============================================
Execution Date: $(date)

Test Results:
- Unit Tests:        $([ "$UNIT_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- Integration Tests: $([ "$INTEGRATION_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- Mutation Tests:    $([ "$MUTATION_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- Smoke Tests:       $([ "$SMOKE_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- Load Tests:        $([ "$LOAD_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- Security Tests:    $([ "$SECURITY_TESTS_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")

Generated Reports:
- Coverage Report:   htmlcov/index.html
- JUnit Results:     reports/junit.xml
- Smoke Test Report: reports/smoke_test_report.html
- Load Test Report:  reports/load_test_report.html
- Mutation Report:   html/index.html (if run)

EOF

# Final status
echo "================================================================="
if [ "$UNIT_TESTS_PASSED" = true ] && [ "$INTEGRATION_TESTS_PASSED" = true ] && [ "$MUTATION_TESTS_PASSED" = true ]; then
    print_success "🎉 All critical tests passed! Ready for deployment."
    exit 0
else
    print_error "❌ Some tests failed. Review the results before proceeding."
    cat reports/test_summary.txt
    exit 1
fi
