#!/bin/bash

# Script de test automatisé pour Nexus Réussite Backend
echo "🧪 Lancement des tests unitaires - Nexus Réussite Backend"
echo "=========================================================="

# Configuration
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend
source /home/alaeddine/Documents/NSI_cours_accompagnement/.venv/bin/activate

echo "📋 Configuration de l'environnement..."
export FLASK_ENV=testing
export OPENAI_API_KEY=test-key-for-testing

echo "🔍 Collecte des tests..."
TEST_COUNT=$(python -m pytest --collect-only -q 2>/dev/null | grep -c "test_")
echo "   ✅ $TEST_COUNT tests détectés"

echo ""
echo "🎯 Exécution des tests prioritaires..."

# Test 1: Health check simple
echo "   🏥 Test Health Check..."
if timeout 10 python -m pytest tests/test_main_api.py::TestMainAPI::test_health_check -v --tb=no -q >/dev/null 2>&1; then
    echo "      ✅ Health Check - RÉUSSI"
    HEALTH_OK=1
else
    echo "      ❌ Health Check - ÉCHEC"
    HEALTH_OK=0
fi

# Test 2: Modèle User
echo "   👤 Test Modèle User..."
if timeout 10 python -m pytest tests/unit/models/test_user.py::TestUserModel::test_user_creation_with_valid_data -v --tb=no -q >/dev/null 2>&1; then
    echo "      ✅ Modèle User - RÉUSSI"
    USER_OK=1
else
    echo "      ❌ Modèle User - ÉCHEC"
    USER_OK=0
fi

# Test 3: Fixture database
echo "   🗃️  Test Base de données..."
if timeout 10 python -m pytest tests/test_main_api.py::TestIntegration::test_database_connection -v --tb=no -q >/dev/null 2>&1; then
    echo "      ✅ Base de données - RÉUSSI"
    DB_OK=1
else
    echo "      ❌ Base de données - ÉCHEC"
    DB_OK=0
fi

echo ""
echo "📊 Résumé des tests:"
echo "==================="
echo "   Health Check:     $([ $HEALTH_OK -eq 1 ] && echo "✅ RÉUSSI" || echo "❌ ÉCHEC")"
echo "   Modèle User:      $([ $USER_OK -eq 1 ] && echo "✅ RÉUSSI" || echo "❌ ÉCHEC")"
echo "   Base de données:  $([ $DB_OK -eq 1 ] && echo "✅ RÉUSSI" || echo "❌ ÉCHEC")"

# Score final
TOTAL_TESTS=3
PASSED_TESTS=$((HEALTH_OK + USER_OK + DB_OK))
PERCENTAGE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo ""
echo "🎯 Score Final: $PASSED_TESTS/$TOTAL_TESTS tests réussis ($PERCENTAGE%)"

if [ $PERCENTAGE -ge 70 ]; then
    echo "🎉 Infrastructure de tests opérationnelle !"
    exit 0
else
    echo "⚠️  Infrastructure nécessite des corrections"
    echo ""
    echo "📝 Diagnostic détaillé:"
    python -m pytest tests/test_main_api.py::TestMainAPI::test_health_check --tb=short -v
    exit 1
fi
