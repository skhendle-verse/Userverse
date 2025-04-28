#!/bin/bash

set -e  # Exit on error (but we'll handle test collection issues manually)
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

# ✅ Function to safely run tests if the file exists
check_and_run_tests() {
    TEST_LABEL=$1
    TEST_PATH=$2
    echo "-----------------------------------------"
    echo "$TEST_LABEL"
    if [ -f "$TEST_PATH" ]; then
        pytest -v --cov=app --cov-append --cov-report=xml:"$COVERAGE_DIR/coverage.xml" "$TEST_PATH" || true
    else
        echo "⚠️  Skipping: $TEST_PATH not found."
    fi
}

# Start testing sections using the helper function
check_and_run_tests "🧪 Main route testing..." "tests/http/test_main.py"
check_and_run_tests "🔐 Security testing..." "tests/http/test_security.py"
check_and_run_tests "👤 Create user testing..." "tests/http/user/test_a_create_user_api.py"
check_and_run_tests "🔑 User login testing..." "tests/http/user/test_b_user_login_api.py"
check_and_run_tests "📥 Get user testing..." "tests/http/user/test_c_get_user.py"
check_and_run_tests "✏️ Update user testing..." "tests/http/user/test_d_update_user_api.py"

echo "-----------------------------------------"
echo "📄 Generating Coverage Report Summary:"
pytest --cov=app --cov-report=term-missing

echo "========================================="
echo "✅ HTTP integration tests completed!"
echo "📁 Coverage report saved to: $COVERAGE_DIR/coverage.xml"
echo "========================================="
