#!/bin/bash

# Script to update requirements.lock file
# This ensures deterministic builds by freezing exact dependency versions

echo "🔄 Updating requirements.lock file..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Error: Please activate your virtual environment first"
    echo "   Run: source .venv/bin/activate"
    exit 1
fi

# Check if requirements.txt exists
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check for dependency conflicts
echo "🔍 Checking for dependency conflicts..."
if ! pip check; then
    echo "❌ Error: Dependency conflicts detected. Please resolve them before generating the lock file."
    exit 1
fi

# Generate lock file
echo "🔒 Generating requirements.lock..."
pip freeze > requirements.lock

echo "✅ Successfully updated requirements.lock"
echo "📝 Don't forget to commit both requirements.txt and requirements.lock files"
