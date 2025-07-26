"""
Flask Application Factory Entry Point
Simple wrapper for src.main_production.create_app for easier deployment
"""

from src.main_production import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run()
