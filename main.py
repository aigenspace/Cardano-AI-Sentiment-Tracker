from endpoint import SentimentEndpoint
from flask import Flask

if __name__ == "__main__":
    # Start the Flask application
    app = Flask(__name__)
    ui = SentimentEndpoint(app)
    ui.setup_routes()
    app.run(debug=True)
