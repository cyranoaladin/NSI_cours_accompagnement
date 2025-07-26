#!/bin/bash

# Nexus Réussite Backend Deployment Script
# Production deployment automation

set -euo pipefail

# Configuration
NAMESPACE="nexus-reussite"
RELEASE_NAME="nexus-backend"
CHART_PATH="./helm/nexus-reussite-backend"
VALUES_FILE="values-production.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if kubectl is installed and configured
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed"
        exit 1
    fi
    
    # Check if helm is installed
    if ! command -v helm &> /dev/null; then
        log_error "helm is not installed"
        exit 1
    fi
    
    # Check if we can connect to cluster
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create namespace if it doesn't exist
create_namespace() {
    log_info "Creating namespace if not exists..."
    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    log_success "Namespace ${NAMESPACE} is ready"
}

# Deploy secrets
deploy_secrets() {
    log_info "Deploying secrets..."
    
    # Check if secrets file exists
    if [[ ! -f "secrets/${VALUES_FILE}" ]]; then
        log_warning "Secrets file not found at secrets/${VALUES_FILE}"
        log_warning "Make sure to create secrets manually before deployment"
        return
    fi
    
    # Apply secrets
    kubectl apply -f secrets/ -n ${NAMESPACE}
    log_success "Secrets deployed"
}

# Deploy application using Helm
deploy_application() {
    log_info "Deploying application..."
    
    # Update Helm dependencies
    helm dependency update ${CHART_PATH}
    
    # Deploy or upgrade
    if helm list -n ${NAMESPACE} | grep -q ${RELEASE_NAME}; then
        log_info "Upgrading existing release..."
        helm upgrade ${RELEASE_NAME} ${CHART_PATH} \
            --namespace ${NAMESPACE} \
            --values ${CHART_PATH}/${VALUES_FILE} \
            --timeout 10m \
            --wait \
            --atomic
    else
        log_info "Installing new release..."
        helm install ${RELEASE_NAME} ${CHART_PATH} \
            --namespace ${NAMESPACE} \
            --values ${CHART_PATH}/${VALUES_FILE} \
            --timeout 10m \
            --wait \
            --atomic
    fi
    
    log_success "Application deployed successfully"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Wait for deployment to be ready
    kubectl wait --for=condition=available \
        deployment/${RELEASE_NAME}-nexus-reussite-backend \
        -n ${NAMESPACE} \
        --timeout=300s
    
    # Check if pods are running
    RUNNING_PODS=$(kubectl get pods -n ${NAMESPACE} -l app.kubernetes.io/name=nexus-reussite-backend --field-selector=status.phase=Running --no-headers | wc -l)
    
    if [[ ${RUNNING_PODS} -gt 0 ]]; then
        log_success "Health check passed - ${RUNNING_PODS} pods running"
    else
        log_error "Health check failed - no pods running"
        exit 1
    fi
}

# Display deployment info
display_info() {
    log_info "Deployment Information:"
    echo "=========================="
    echo "Namespace: ${NAMESPACE}"
    echo "Release: ${RELEASE_NAME}"
    echo "Chart: ${CHART_PATH}"
    echo "Values: ${VALUES_FILE}"
    echo ""
    
    log_info "Pod Status:"
    kubectl get pods -n ${NAMESPACE} -l app.kubernetes.io/name=nexus-reussite-backend
    
    echo ""
    log_info "Service Status:"
    kubectl get svc -n ${NAMESPACE} -l app.kubernetes.io/name=nexus-reussite-backend
    
    echo ""
    log_info "Ingress Status:"
    kubectl get ingress -n ${NAMESPACE}
}

# Rollback function
rollback() {
    log_warning "Rolling back to previous version..."
    helm rollback ${RELEASE_NAME} -n ${NAMESPACE}
    log_success "Rollback completed"
}

# Main deployment function
main() {
    log_info "Starting Nexus Réussite Backend Deployment"
    log_info "==========================================="
    
    case ${1:-deploy} in
        "deploy")
            check_prerequisites
            create_namespace
            deploy_secrets
            deploy_application
            health_check
            display_info
            ;;
        "rollback")
            check_prerequisites
            rollback
            health_check
            display_info
            ;;
        "status")
            display_info
            ;;
        "health")
            health_check
            ;;
        *)
            echo "Usage: $0 [deploy|rollback|status|health]"
            echo ""
            echo "Commands:"
            echo "  deploy   - Deploy the application (default)"
            echo "  rollback - Rollback to previous version"
            echo "  status   - Show deployment status"
            echo "  health   - Perform health check"
            exit 1
            ;;
    esac
    
    log_success "Deployment script completed successfully"
}

# Trap for cleanup on error
trap 'log_error "Deployment script failed"; exit 1' ERR

# Run main function
main "$@"
