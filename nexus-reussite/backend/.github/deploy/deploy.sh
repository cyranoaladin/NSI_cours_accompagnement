#!/bin/bash

# Nexus Réussite Backend Deployment Script
# Usage: ./deploy.sh [staging|production] [image_tag]

set -e

ENVIRONMENT=${1:-staging}
IMAGE_TAG=${2:-latest}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

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

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    log_error "Invalid environment: $ENVIRONMENT. Must be 'staging' or 'production'"
    exit 1
fi

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Please install kubectl."
        exit 1
    fi
    
    if ! command -v helm &> /dev/null; then
        log_warning "helm not found. Some features may not work."
    fi
    
    # Test kubectl connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster. Check your kubeconfig."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create namespace if it doesn't exist
create_namespace() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Creating namespace: $namespace"
    
    kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f -
    kubectl label namespace "$namespace" environment="$ENVIRONMENT" --overwrite
    
    log_success "Namespace $namespace ready"
}

# Deploy secrets (in real deployment, these would come from a secure source)
deploy_secrets() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Deploying secrets to $namespace..."
    
    # Check if secrets already exist
    if kubectl get secret nexus-secrets -n "$namespace" &> /dev/null; then
        log_info "Secrets already exist, skipping creation"
        return
    fi
    
    # Create secrets (replace with your actual secret values)
    kubectl create secret generic nexus-secrets \
        -n "$namespace" \
        --from-literal=database-url="${DATABASE_URL:-postgresql://user:pass@postgres:5432/nexus}" \
        --from-literal=redis-url="${REDIS_URL:-redis://redis:6379/0}" \
        --from-literal=secret-key="${SECRET_KEY:-your-secret-key}" \
        --from-literal=openai-api-key="${OPENAI_API_KEY:-your-openai-key}" \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "Secrets deployed"
}

# Update deployment with new image
update_deployment() {
    local namespace="nexus-${ENVIRONMENT}"
    local image="ghcr.io/nexus-reussite/backend:${IMAGE_TAG}"
    
    log_info "Updating deployment in $namespace with image: $image"
    
    # Apply the kubernetes manifests
    envsubst < "$SCRIPT_DIR/kubernetes.yml" | kubectl apply -f -
    
    # Update the image
    kubectl set image deployment/nexus-backend nexus-backend="$image" -n "$namespace"
    
    log_success "Deployment updated"
}

# Wait for deployment to be ready
wait_for_deployment() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Waiting for deployment to be ready..."
    
    if kubectl rollout status deployment/nexus-backend -n "$namespace" --timeout=600s; then
        log_success "Deployment rolled out successfully"
    else
        log_error "Deployment rollout failed"
        kubectl describe deployment/nexus-backend -n "$namespace"
        kubectl logs -l app=nexus-backend -n "$namespace" --tail=50
        exit 1
    fi
}

# Run health check
health_check() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Running health check..."
    
    # Port forward to test the service
    kubectl port-forward service/nexus-backend-service 8080:80 -n "$namespace" &
    PORT_FORWARD_PID=$!
    
    sleep 5
    
    # Test the health endpoint
    if curl -f http://localhost:8080/health &> /dev/null; then
        log_success "Health check passed"
    else
        log_error "Health check failed"
        kill $PORT_FORWARD_PID 2>/dev/null || true
        exit 1
    fi
    
    kill $PORT_FORWARD_PID 2>/dev/null || true
}

# Run smoke tests
smoke_tests() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Running smoke tests..."
    
    # Create a test pod
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: smoke-test
  namespace: $namespace
spec:
  containers:
  - name: curl
    image: curlimages/curl:latest
    command: ['sleep', '300']
  restartPolicy: Never
EOF

    # Wait for pod to be ready
    kubectl wait --for=condition=Ready pod/smoke-test -n "$namespace" --timeout=60s
    
    # Run smoke tests
    local service_url="http://nexus-backend-service.${namespace}.svc.cluster.local"
    
    if kubectl exec smoke-test -n "$namespace" -- curl -f "$service_url/health"; then
        log_success "Smoke tests passed"
    else
        log_error "Smoke tests failed"
        kubectl delete pod smoke-test -n "$namespace" --ignore-not-found=true
        exit 1
    fi
    
    # Clean up test pod
    kubectl delete pod smoke-test -n "$namespace" --ignore-not-found=true
}

# Main deployment function
deploy() {
    log_info "Starting deployment to $ENVIRONMENT environment"
    log_info "Using image tag: $IMAGE_TAG"
    
    check_prerequisites
    create_namespace
    deploy_secrets
    update_deployment
    wait_for_deployment
    health_check
    smoke_tests
    
    log_success "Deployment to $ENVIRONMENT completed successfully!"
    
    # Show deployment info
    local namespace="nexus-${ENVIRONMENT}"
    echo ""
    log_info "Deployment Summary:"
    kubectl get pods -n "$namespace" -l app=nexus-backend
    kubectl get services -n "$namespace"
    kubectl get ingress -n "$namespace"
}

# Rollback function
rollback() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Rolling back deployment in $namespace..."
    
    kubectl rollout undo deployment/nexus-backend -n "$namespace"
    kubectl rollout status deployment/nexus-backend -n "$namespace" --timeout=300s
    
    log_success "Rollback completed"
}

# Show deployment status
status() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Deployment status for $ENVIRONMENT:"
    
    kubectl get all -n "$namespace" -l app=nexus-backend
    kubectl describe deployment/nexus-backend -n "$namespace"
}

# Show logs
logs() {
    local namespace="nexus-${ENVIRONMENT}"
    log_info "Recent logs from $ENVIRONMENT:"
    
    kubectl logs -l app=nexus-backend -n "$namespace" --tail=100 -f
}

# Handle script arguments
case "${3:-deploy}" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "Usage: $0 [staging|production] [image_tag] [deploy|rollback|status|logs]"
        exit 1
        ;;
esac
