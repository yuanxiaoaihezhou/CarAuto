#!/bin/bash
# Validation script for CarAuto

echo "=== CarAuto Validation Script ==="
echo

echo "1. Checking Python syntax..."
python3 -m py_compile backend/app/config.py backend/app/music_player.py \
    backend/app/settings_manager.py backend/app/driver_monitor.py \
    backend/app/voice_recognizer.py backend/app.py 2>&1
if [ $? -eq 0 ]; then
    echo "✓ All Python files syntax valid"
else
    echo "✗ Python syntax errors found"
    exit 1
fi

echo
echo "2. Checking JavaScript syntax..."
node -c frontend/static/js/app.js 2>&1
if [ $? -eq 0 ]; then
    echo "✓ JavaScript syntax valid"
else
    echo "✗ JavaScript syntax errors found"
    exit 1
fi

echo
echo "3. Checking HTML..."
if [ -f frontend/templates/index.html ]; then
    echo "✓ HTML template exists"
else
    echo "✗ HTML template missing"
    exit 1
fi

echo
echo "4. Checking CSS..."
if [ -f frontend/static/css/style.css ]; then
    echo "✓ CSS stylesheet exists"
else
    echo "✗ CSS stylesheet missing"
    exit 1
fi

echo
echo "5. Checking documentation..."
docs=("README.md" "docs/README.md" "docs/API.md" "docs/ARCHITECTURE.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✓ $doc exists"
    else
        echo "✗ $doc missing"
        exit 1
    fi
done

echo
echo "6. Checking tests..."
if [ -d backend/tests ]; then
    test_count=$(find backend/tests -name "test_*.py" | wc -l)
    echo "✓ Found $test_count test files"
else
    echo "✗ Tests directory missing"
    exit 1
fi

echo
echo "7. Checking project structure..."
required_dirs=("backend" "backend/app" "backend/tests" "frontend" "frontend/static" "frontend/templates" "data" "docs")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "✗ $dir missing"
        exit 1
    fi
done

echo
echo "=== All validations passed! ==="
echo
echo "To run the application:"
echo "1. Install dependencies: pip install -r backend/requirements.txt"
echo "2. Add music files to data/music/"
echo "3. Run: python backend/app.py"
echo "4. Open browser: http://localhost:5000"
