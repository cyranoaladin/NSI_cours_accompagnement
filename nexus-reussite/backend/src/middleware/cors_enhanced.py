#!/usr/bin/env python3
"""CORS Enhanced Middleware for Production"""

from flask_cors import CORS

def enhanced_cors(app):
    """Configuration CORS optimisée pour production"""
    CORS(app,
         origins=["http://localhost:3000", "https://nexus-reussite.com"],
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])
    return app

def setup_cors(app):
    """Alias pour compatibilité"""
    return enhanced_cors(app)
