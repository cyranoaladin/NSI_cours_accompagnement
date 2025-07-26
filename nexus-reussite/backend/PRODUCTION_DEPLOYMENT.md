# Nexus Réussite Backend - Production Deployment Guide

## Overview

This guide covers the production deployment of Nexus Réussite Backend with all optimizations and hardening measures implemented in Step 9.

## Production Features Implemented

### ✅ Gunicorn Configuration
- **Default entrypoint**: `gunicorn -k gevent -w 4 'src.app:create_app()'`
- Optimized worker configuration with gevent for async support
- Connection pooling and request limits
- Proper timeout and keep-alive settings

### ✅ Compression
- **Flask-Compress** integrated for response compression
- Configurable compression level and minimum size
- Multiple MIME types supported (HTML, CSS, JS, JSON, etc.)

### ✅ Security Hardening
- **Flask-Talisman** for HTTPS enforcement and security headers
- **HSTS** (HTTP Strict Transport Security) with 1-year max-age
- **Secure cookies** with HttpOnly and SameSite attributes
- **CSP** (Content Security Policy) for XSS protection
- **Referrer Policy** and **Feature Policy** configured

### ✅ Performance Optimization
- **SQLAlchemy connection pooling** tuned for production
  - Pool size: 20 connections
  - Pool timeout: 60 seconds
  - Pool recycle: 1 hour
  - Max overflow: 30 connections
- **Redis cache TTLs** optimized by data type
  - Short: 10 minutes
  - Medium: 2 hours
  - Long: 24 hours
- **Enhanced rate limiting** for production load

### ✅ Error Tracking
- **Sentry DSN** integration for production error monitoring
- Configurable sampling rates for traces and profiling
- Flask and SQLAlchemy integrations

## Quick Start

### 1. Environment Setup

```bash
# Copy the production environment template
cp .env.production.template .env.production

# Edit the file with your production values
nano .env.production
```

### 2. Required Environment Variables

```bash
# Critical - Must be configured
FLASK_ENV=production
SECRET_KEY=your-unique-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/db

# Optional but recommended
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
OPENAI_API_KEY=your-openai-api-key
```

### 3. Docker Deployment

```bash
# Build production image
docker build -f Dockerfile.production -t nexus-reussite-backend:prod .

# Run with environment file
docker run -d \
  --name nexus-backend \
  --env-file .env.production \
  -p 5000:5000 \
  nexus-reussite-backend:prod
```

### 4. Health Checks

The application provides comprehensive health check endpoints:

- **Liveness**: `GET /live` - Basic application responsiveness
- **Readiness**: `GET /ready` - Database connectivity and full initialization
- **Health**: `GET /health` - Complete system health with metrics

### 5. Monitoring

- **Prometheus metrics**: Available at `/metrics`
- **Application logs**: Structured JSON logging
- **Sentry monitoring**: Error tracking and performance monitoring

## Configuration Details

### Database Connection Pool

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,           # Max connections in pool
    'pool_timeout': 60,        # Timeout to get connection
    'pool_recycle': 3600,      # Recycle connections every hour
    'max_overflow': 30,        # Max overflow connections
    'pool_pre_ping': True,     # Validate connections
}
```

### Cache TTL Strategy

```python
CACHE_TTL_SHORT = 600      # User sessions, temporary data
CACHE_TTL_MEDIUM = 7200    # API responses, computed data
CACHE_TTL_LONG = 86400     # Static content, configs
```

### Rate Limiting (Production)

```python
RATELIMIT_DEFAULT = "1000 per day;100 per hour;2 per second"
```

### Security Headers

- **HSTS**: 1 year with subdomain inclusion
- **CSP**: Strict policy with necessary exceptions
- **Secure Cookies**: HttpOnly, Secure, SameSite=Lax
- **Referrer Policy**: strict-origin-when-cross-origin

## Performance Tuning

### Gunicorn Workers

For optimal performance, adjust worker count based on your server:

```bash
# CPU-bound: workers = (2 x CPU cores) + 1
# I/O-bound: workers = (4 x CPU cores) + 1

# Example for 4-core server
gunicorn -k gevent -w 17 'src.app:create_app()'
```

### Redis Configuration

Recommended Redis settings for production:

```redis
# In redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### PostgreSQL Tuning

Recommended PostgreSQL settings:

```postgresql
# In postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
max_connections = 100
```

## Security Checklist

### ✅ Pre-deployment Security

- [ ] Change all default secrets and keys
- [ ] Configure HTTPS certificates
- [ ] Set up firewall rules
- [ ] Configure CORS origins for your domain
- [ ] Enable Sentry error tracking
- [ ] Set up database user with minimal privileges
- [ ] Configure Redis authentication
- [ ] Review and test backup procedures

### ✅ Runtime Security

- [ ] Monitor error rates and response times
- [ ] Check security headers with tools like securityheaders.com
- [ ] Regularly update dependencies
- [ ] Monitor resource usage
- [ ] Review access logs for suspicious activity

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database connectivity
   flask diagnose
   ```

2. **Redis Connection Issues**
   ```bash
   # Test Redis connection
   redis-cli -u $REDIS_URL ping
   ```

3. **High Memory Usage**
   ```bash
   # Monitor workers
   ps aux | grep gunicorn
   ```

4. **Slow Response Times**
   ```bash
   # Check health endpoint
   curl http://localhost:5000/health
   ```

### Debug Mode

Never enable debug mode in production. If needed for troubleshooting:

```bash
# Temporary debug mode (restart required)
export FLASK_ENV=development
export DEBUG=true
```

## Monitoring and Alerts

### Key Metrics to Monitor

- Response time percentiles (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Database connection pool utilization
- Cache hit/miss ratios
- Memory and CPU usage
- Disk space utilization

### Recommended Alerts

- Error rate > 5%
- Response time p95 > 2 seconds
- Database connection pool > 80% utilization
- Memory usage > 85%
- Disk space > 80%

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer Configuration**
   - Use sticky sessions for WebSocket connections
   - Health check on `/ready` endpoint
   - Proper timeout settings

2. **Database Scaling**
   - Read replicas for read-heavy workloads
   - Connection pooling with PgBouncer
   - Database partitioning for large datasets

3. **Cache Scaling**
   - Redis Cluster for high availability
   - Cache warming strategies
   - Proper cache invalidation

### Vertical Scaling

- Monitor CPU and memory usage patterns
- Adjust worker count based on load
- Optimize database queries with indexes
- Use CDN for static assets

## Support

For production support and advanced configuration, please refer to:

- Application logs: `/app/logs/`
- Health endpoint: `/health`
- Metrics endpoint: `/metrics`
- Diagnostic command: `flask diagnose`
