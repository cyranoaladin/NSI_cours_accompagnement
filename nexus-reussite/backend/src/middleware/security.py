#!/usr/bin/env python3
"""Security Middleware for Production"""

from flask import request, jsonify
from functools import wraps

def security_middleware(app):
    """Configuration sécurité avancée pour production"""

    @app.before_request
    def security_headers():
        # Headers de sécurité
        pass

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    return app

def setup_security_headers(app):
    """Alias pour compatibilité"""
    return security_middleware(app)
