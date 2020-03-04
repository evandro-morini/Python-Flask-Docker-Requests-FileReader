from app import app
from flask import jsonify
from ..views import phone


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Phone Aggregator Test'})


@app.route('/aggregate', methods=['POST'])
def aggregate():
    return phone.post_aggregate()