"""Middleware package - Auto-generated"""

# CORS Middleware
def setup_cors(app):
    """Setup CORS for the Flask app"""
    try:
        from flask_cors import CORS
        CORS(app, 
             origins=['http://localhost:5173', 'http://localhost:3000'],
             allow_headers=['Content-Type', 'Authorization'],
             allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    except ImportError:
        # Fallback CORS headers
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

# Security Headers Middleware
def security_headers(app):
    """Add security headers to responses"""
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

# Request Logging Middleware
def request_logging(app):
    """Log all requests"""
    import logging
    logger = logging.getLogger(__name__)
    
    @app.before_request
    def log_request():
        logger.info(f"Request: {app.request.method} {app.request.url}")

# Rate Limiting Middleware (Basic)
def rate_limiting(app):
    """Basic rate limiting"""
    from collections import defaultdict
    from time import time
    
    request_counts = defaultdict(list)
    
    @app.before_request
    def limit_requests():
        import flask
        client_ip = flask.request.environ.get('REMOTE_ADDR')
        now = time()
        
        # Clean old requests (older than 60 seconds)
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip] 
            if now - req_time < 60
        ]
        
        # Check rate limit (max 100 requests per minute)
        if len(request_counts[client_ip]) >= 100:
            flask.abort(429)  # Too Many Requests
        
        request_counts[client_ip].append(now)

def init_middleware(app):
    """Initialize all middleware"""
    setup_cors(app)
    security_headers(app)
    request_logging(app)
    rate_limiting(app)
