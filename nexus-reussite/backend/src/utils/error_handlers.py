"""Error handlers - Auto-generated"""

def setup_error_handlers(app):
    """Setup error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        return {
            "error": "Bad Request",
            "message": "The request could not be understood by the server",
            "status_code": 400
        }, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors"""
        return {
            "error": "Unauthorized",
            "message": "Authentication required",
            "status_code": 401
        }, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors"""
        return {
            "error": "Forbidden",
            "message": "You don't have permission to access this resource",
            "status_code": 403
        }, 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        return {
            "error": "Not Found",
            "message": "The requested resource was not found",
            "status_code": 404
        }, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit errors"""
        return {
            "error": "Rate Limit Exceeded",
            "message": "Too many requests, please try again later",
            "status_code": 429
        }, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        return {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        import logging
        logger = logging.getLogger(__name__)
        logger.error("Unhandled exception: %s", str(error))
        
        return {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }, 500
