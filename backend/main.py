from app import create_app
from config import config
import os

if __name__ == "__main__":
    env = os.getenv('FLASK_ENV', 'default')
    app = create_app(config_class=config[env])

    # No need to call CORS(app) again since it’s already set in create_app
    app.run(host="0.0.0.0", port=5000, debug=config[env].DEBUG)
