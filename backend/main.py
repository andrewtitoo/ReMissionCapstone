from app import create_app
from config import config
import os

if __name__ == "__main__":
    # Determine the environment and Load the appropriate configuration
    env = os.getenv('FLASK_ENV', 'default')
    app = create_app(config_class=config[env])

    # Run the app on host 0.0.0.0 to be accessible on local network
    app.run(host="0.0.0.0", port=5000, debug=config[env].DEBUG)