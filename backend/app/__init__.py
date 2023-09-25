from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from your_script_file import fetch_and_store_data

def create_app():
    app = Flask(__name__)
   # app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Enable CORS for your React app (adjust origins to match your setup)
   # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Schedule the data retrieval job
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_data, "cron", hour="11-14", minute="15", second="0")
    scheduler.start()

    # Import and register your API routes
    from . import routes
    app.register_blueprint(routes.api_bp, url_prefix='/api')

    return app
