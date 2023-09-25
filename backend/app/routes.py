from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/fetch-data', methods=['POST'])
def fetch_data():
    # Trigger the data retrieval process
    fetch_and_store_data()
    return {'message': 'Data retrieval process started.'}, 200
