"""
Main entry point for Nexus Réussite Backend
"""

from main_production import create_app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    app.run()
