from flask_cors import CORS
from app import create_app
from config import config
import os

if __name__ == "__main__":
    env = os.getenv('FLASK_ENV', 'default')
    app = create_app(config_class=config[env])
    CORS(app)  # Enable CORS globally
    app.run(host="0.0.0.0", port=5000, debug=config[env].DEBUG)
