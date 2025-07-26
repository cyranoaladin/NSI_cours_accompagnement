# CI/CD Pipeline Documentation - Nexus Réussite Backend

## Overview

This document describes the complete Continuous Integration and Continuous Delivery (CI/CD) pipeline for the Nexus Réussite backend application. The pipeline follows the modern DevOps practices with automated testing, security scanning, and deployment stages.

## Pipeline Architecture

The CI/CD pipeline consists of the following stages:

1. **Lint** → Code quality checks and formatting validation
2. **Test** → Comprehensive testing suite with coverage reporting  
3. **Build-Image** → Docker image creation and registry push
4. **Security Scan** → Vulnerability assessment and security analysis
5. **Deploy** → Automated deployment to staging/production environments

## Workflow Files

### 1. Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

The primary workflow that runs on every push and pull request:

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Git tags starting with `v*`

**Features:**
- ✅ **Pip wheel caching** for faster builds
- ✅ **Multi-platform Docker builds** (AMD64 + ARM64)  
- ✅ **Security scans** with Bandit, Safety, and Trivy
- ✅ **Automated deployment** to staging and production
- ✅ **Comprehensive test coverage** reporting

### 2. Security Audit (`.github/workflows/security-audit.yml`)

Dedicated security scanning workflow:

**Triggers:**
- Daily scheduled run at 2 AM UTC
- Changes to dependency files
- Manual trigger

**Security Tools:**
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability scanner
- **pip-audit** - PyPI vulnerability database check
- **CodeQL** - Semantic code analysis
- **Semgrep** - Static analysis security scanner

### 3. Performance Testing (`.github/workflows/performance-test.yml`)

Performance and load testing pipeline:

**Triggers:**
- Weekly scheduled run (Sundays at 3 AM UTC)
- Push to main branch affecting core code
- Manual trigger with configurable parameters

**Features:**
- **Locust load testing** with configurable users and duration
- **Memory profiling** with threshold monitoring
- **Performance regression detection**

## Pipeline Stages Detail

### Stage 1: Lint

**Purpose:** Ensure code quality and consistency

**Tools Used:**
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Style guide enforcement
- **pylint** - Static code analysis
- **mypy** - Type checking

**Cache Strategy:**
```yaml
key: ${{ runner.os }}-pip-lint-${{ hashFiles('**/requirements-dev.txt') }}
```

### Stage 2: Test

**Purpose:** Validate application functionality and reliability

**Environment:**
- PostgreSQL 15 database
- Redis 7 cache
- Python 3.12 runtime

**Test Types:**
- Unit tests (`tests/unit/`)
- Integration tests (`tests/integration/`)
- Coverage reporting with 90% threshold

**Artifacts:**
- Test results (JUnit XML)
- Coverage reports (HTML + XML)
- Uploaded to Codecov for tracking

### Stage 3: Build Docker Image

**Purpose:** Create production-ready container images

**Features:**
- Multi-stage Docker build for optimized image size
- Multi-platform builds (AMD64, ARM64)
- GitHub Container Registry (GHCR) as image registry
- Build cache optimization using GitHub Actions cache

**Image Tagging Strategy:**
- `latest` - Latest from main branch
- `develop` - Latest from develop branch  
- `{branch}-{sha}` - Branch-specific builds
- `v{version}` - Semantic version tags

### Stage 4: Security Scan

**Purpose:** Identify vulnerabilities and security issues

**Code Analysis:**
- **Bandit** scans for common security issues in Python code
- **Safety** checks dependencies against vulnerability databases
- **Semgrep** performs pattern-based security analysis

**Container Analysis:**
- **Trivy** scans Docker images for vulnerabilities
- Results uploaded to GitHub Security tab as SARIF

**Failure Handling:**
- Security issues create GitHub issues automatically
- SARIF reports integrate with GitHub Security tab

### Stage 5: Deploy

**Purpose:** Automated deployment to target environments

**Environments:**
- **Staging** (`develop` branch) → `staging-api.nexus-reussite.com`
- **Production** (`main` branch) → `api.nexus-reussite.com`

**Deployment Features:**
- Kubernetes-based deployment
- Rolling updates with zero downtime
- Health checks and smoke tests
- Automatic rollback on failure

## Deployment Architecture

### Kubernetes Resources

**Staging Environment:**
- Namespace: `nexus-staging`
- Replicas: 2 pods
- Resources: 512Mi RAM, 250m CPU (requests)
- Ingress: SSL termination with Let's Encrypt

**Production Environment:**
- Namespace: `nexus-production`  
- Replicas: 3 pods (with HPA scaling to 10)
- Resources: 1Gi RAM, 500m CPU (requests)
- Ingress: SSL + rate limiting
- Auto-scaling based on CPU/memory utilization

### Secrets Management

Application secrets are stored as Kubernetes secrets:
- `database-url` - PostgreSQL connection string
- `redis-url` - Redis connection string  
- `secret-key` - Flask application secret
- `openai-api-key` - OpenAI API credentials

## Cache Strategy

The pipeline implements aggressive caching to minimize build times:

1. **Pip Wheel Cache**: Caches Python package wheels
2. **Docker Layer Cache**: Uses GitHub Actions cache for Docker builds
3. **Test Dependency Cache**: Separate cache for test dependencies

**Cache Keys Pattern:**
```
${{ runner.os }}-pip-{stage}-${{ hashFiles('requirements-files') }}
```

## Security Features

### Dependency Security
- Daily automated security audits
- Vulnerability scanning with multiple tools
- Automatic issue creation for security findings
- Integration with GitHub Security tab

### Container Security  
- Multi-stage Docker builds reduce attack surface
- Non-root user execution in containers
- Minimal base images (Alpine Linux)
- Regular vulnerability scanning with Trivy

### Secret Management
- No secrets in code or configuration files
- Kubernetes secret management
- Environment-specific secret isolation

## Monitoring and Observability

### Build Monitoring
- Comprehensive step summaries in GitHub Actions
- Artifact retention for debugging
- Performance metrics tracking

### Deployment Monitoring
- Health checks with liveness/readiness probes
- Application metrics via Prometheus (production)
- Log aggregation and monitoring

## Usage Instructions

### Running the Pipeline

**Automatic Triggers:**
```bash
# Trigger full pipeline
git push origin main

# Trigger PR validation
git checkout -b feature/new-feature
git push origin feature/new-feature
# Create PR to main/develop
```

**Manual Triggers:**
```bash
# Security audit
gh workflow run security-audit.yml

# Performance testing
gh workflow run performance-test.yml -f duration=600 -f users=100
```

### Deployment Commands

**Using the deployment script:**
```bash
# Deploy to staging
.github/deploy/deploy.sh staging latest

# Deploy to production  
.github/deploy/deploy.sh production v1.2.3

# Check deployment status
.github/deploy/deploy.sh production latest status

# View logs
.github/deploy/deploy.sh staging latest logs

# Rollback deployment
.github/deploy/deploy.sh production latest rollback
```

### Environment Setup

**Required Secrets:**
```bash
# GitHub repository secrets
GITHUB_TOKEN        # Automatically provided
DATABASE_URL        # PostgreSQL connection
REDIS_URL          # Redis connection  
SECRET_KEY         # Application secret
OPENAI_API_KEY     # OpenAI API key
```

**Required Permissions:**
- `contents: read` - Repository access
- `packages: write` - Container registry push
- `security-events: write` - Security scan uploads

## Best Practices

### Code Quality
1. Follow Black formatting standards
2. Maintain test coverage above 90%
3. Fix security issues promptly
4. Keep dependencies updated

### Pipeline Maintenance
1. Review pipeline performance monthly
2. Update action versions quarterly  
3. Monitor security scan results
4. Optimize cache usage

### Deployment Safety
1. Always deploy to staging first
2. Run comprehensive tests before production
3. Monitor application health post-deployment
4. Keep rollback procedures tested and ready

## Troubleshooting

### Common Issues

**Build Failures:**
- Check dependency compatibility
- Verify Python version consistency
- Review test failures in artifacts

**Security Scan Failures:**
- Update vulnerable dependencies
- Review and acknowledge false positives
- Check CVE databases for impact

**Deployment Failures:**
- Verify Kubernetes cluster connectivity
- Check secret availability
- Review resource limits and quotas
- Examine pod logs for application errors

### Debug Commands

```bash
# Check pipeline status
gh run list --workflow=ci-cd.yml

# Download artifacts
gh run download [run-id]

# View deployment logs
kubectl logs -n nexus-staging -l app=nexus-backend --tail=100

# Check service health
kubectl port-forward -n nexus-staging svc/nexus-backend-service 8080:80
curl http://localhost:8080/health
```

## Performance Metrics

### Pipeline Performance
- **Average build time**: ~15 minutes
- **Cache hit rate**: 85%+ for dependencies
- **Security scan duration**: ~5 minutes
- **Deployment time**: ~3 minutes

### Application Performance
- **Load test capacity**: 100 concurrent users
- **Response time**: <200ms (95th percentile)
- **Memory usage**: <500MB per pod
- **CPU utilization**: <50% under normal load

## Future Enhancements

### Planned Improvements
1. **GitOps Integration**: Implement Argo CD for deployment management
2. **Blue-Green Deployments**: Zero-downtime deployment strategy
3. **Advanced Monitoring**: Implement distributed tracing
4. **Multi-Region**: Deploy across multiple geographical regions
5. **Chaos Engineering**: Implement chaos testing in staging

### Monitoring Roadmap
1. **SLI/SLO Definition**: Establish service level objectives
2. **Alert Management**: Implement comprehensive alerting
3. **Performance Budgets**: Set and monitor performance thresholds
4. **Cost Monitoring**: Track infrastructure costs and optimization

---

## Support

For questions or issues with the CI/CD pipeline:

1. **GitHub Issues**: Create an issue in the repository
2. **Documentation**: Check this document and inline comments
3. **Team Contact**: Reach out to the DevOps team

**Pipeline Status**: ![CI/CD Status](https://github.com/nexus-reussite/backend/workflows/CI%2FCD%20Pipeline/badge.svg)
