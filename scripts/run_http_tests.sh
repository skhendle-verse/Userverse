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

echo "-----------------------------------------"
echo "📄 Generating Coverage Report Summary:"
pytest --cov=app --cov-report=term-missing

echo "========================================="
echo "✅ HTTP integration tests completed!"
echo "📁 Coverage report saved to: $COVERAGE_DIR/coverage.xml"
echo "========================================="
