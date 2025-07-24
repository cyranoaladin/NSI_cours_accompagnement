#!/bin/bash

# Script avancé de tests pour identifier tous les problèmes
echo "🔍 DIAGNOSTIC COMPLET DES TESTS - NEXUS RÉUSSITE"
echo "================================================"

cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite-backend
source /home/alaeddine/Documents/NSI_cours_accompagnement/.venv/bin/activate

export FLASK_ENV=testing
export OPENAI_API_KEY=test-key-for-testing

echo ""
echo "📋 Tests individuels détaillés:"
echo "==============================="

# Liste des tests à tester individuellement
TESTS=(
    "tests/test_main_api.py::TestMainAPI::test_health_check"
    "tests/test_main_api.py::TestMainAPI::test_api_health_check"
    "tests/test_main_api.py::TestMainAPI::test_config_info"
    "tests/test_main_api.py::TestMainAPI::test_cors_headers"
    "tests/test_main_api.py::TestMainAPI::test_rate_limiting"
    "tests/test_main_api.py::TestMainAPI::test_nonexistent_api_endpoint"
    "tests/test_main_api.py::TestMainAPI::test_frontend_fallback"
    "tests/test_main_api.py::TestMainAPI::test_static_assets_route"
    "tests/unit/models/test_user.py::TestUserModel::test_user_creation_with_valid_data"
    "tests/unit/models/test_user.py::TestUserModel::test_user_full_name_property"
    "tests/unit/models/test_user.py::TestUserModel::test_password_hashing_and_verification"
)

PASSED=0
FAILED=0
TIMEOUT=0

for test in "${TESTS[@]}"; do
    echo -n "   Testing: $(basename "$test")... "
    
    if timeout 10 python -m pytest "$test" -v --tb=no -q >/dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo "⏰ TIMEOUT"
            ((TIMEOUT++))
        else
            echo "❌ FAIL"
            ((FAILED++))
        fi
    fi
done

echo ""
echo "📊 Résumé détaillé:"
echo "==================="
echo "   ✅ Réussis:  $PASSED"
echo "   ❌ Échoués:   $FAILED"
echo "   ⏰ Timeouts:  $TIMEOUT"
echo ""

TOTAL=$((PASSED + FAILED + TIMEOUT))
if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$((PASSED * 100 / TOTAL))
    echo "🎯 Taux de réussite: $SUCCESS_RATE%"
else
    echo "⚠️  Aucun test exécuté"
    exit 1
fi

echo ""
echo "🧪 Test de collecte complète:"
echo "============================="
echo -n "   Collecte de tous les tests... "

if timeout 5 python -m pytest --collect-only -q >/dev/null 2>&1; then
    TEST_COUNT=$(python -m pytest --collect-only -q 2>/dev/null | grep -c "test_" || echo "0")
    echo "✅ $TEST_COUNT tests détectés"
else
    echo "❌ Erreur de collecte"
fi

echo ""
if [ $SUCCESS_RATE -ge 90 ]; then
    echo "🎉 INFRASTRUCTURE EXCELLENTE - Prête pour la production !"
    exit 0
elif [ $SUCCESS_RATE -ge 70 ]; then
    echo "✅ Infrastructure fonctionnelle - Quelques ajustements nécessaires"
    exit 0
else
    echo "⚠️  Infrastructure nécessite des corrections importantes"
    
    echo ""
    echo "🔧 Diagnostics pour les tests échoués:"
    if [ $FAILED -gt 0 ]; then
        echo "   Exécution d'un test échoué avec détails:"
        timeout 10 python -m pytest "${TESTS[0]}" -v --tb=short
    fi
    exit 1
fi
