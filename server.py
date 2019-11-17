from flask import Flask, request, jsonify
from weather import get_weather_data

app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive_data():
    req_data = request.json
    get_weather_data(req_data)
    # print (req_data['queryResult']['parameters']['geo-city'])
    return 'data received'
