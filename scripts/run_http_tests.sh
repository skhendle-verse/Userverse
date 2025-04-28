#!/bin/bash

set -e  # Exit on error
set -o pipefail

echo "========================================="
echo "🚀 Starting HTTP Integration Test Suite"
echo "========================================="

# Export environment variable for test mode
export TEST_ENVIRONMENT=True
echo "✅ TEST_ENVIRONMENT set to True"

# Optional: Clean up old test DB if exists
if [ -f "testing.db" ]; then
    echo "🗑️ Removing old testing.db..."
    rm testing.db
fi

# Optional: Setup coverage report directory
COVERAGE_DIR="coverage_reports"
mkdir -p "$COVERAGE_DIR"

# Start testing sections
echo "-----------------------------------------"
echo "🧪 Main route testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/test_main.py

echo "-----------------------------------------"
echo "🔐 Security testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/test_security.py

echo "-----------------------------------------"
echo "👤 Create user testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/user/test_a_create_user_api.py

echo "-----------------------------------------"
echo "🔑 User login testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/user/test_b_user_login_api.py

echo "-----------------------------------------"
echo "📥 Get user testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/user/test_c_get_user.py

echo "-----------------------------------------"
echo "✏️ Update user testing..."
pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" tests/http/user/test_d_update_user_api.py

echo "-----------------------------------------"
echo "📄 Generating Coverage Report Summary:"
pytest --cov=app --cov-report=term-missing

echo "========================================="
echo "✅ HTTP integration tests completed!"
echo "📁 Coverage report saved to: $COVERAGE_DIR/coverage.xml"
echo "========================================="
