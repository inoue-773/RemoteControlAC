from flask import Flask, jsonify, request
import subprocess
import cgsensor
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the BME280 sensor
bme280 = cgsensor.BME280(i2c_addr=0x76)

# Get the required password from the environment variables
REQUIRED_PASSWORD = os.getenv('PASSWORD')

# Helper function to check password
def check_password():
    password = request.headers.get("Password")
    if not password or password != REQUIRED_PASSWORD:
        return False
    return True

@app.route('/temperature', methods=['GET'])
def get_temperature():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    bme280.forced()
    temperature = bme280.temperature
    return jsonify({'temperature': temperature})

@app.route('/humidity', methods=['GET'])
def get_humidity():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    bme280.forced()
    humidity = bme280.humidity
    return jsonify({'humidity': humidity})

@app.route('/pressure', methods=['GET'])
def get_pressure():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    bme280.forced()
    pressure = bme280.pressure
    return jsonify({'pressure': pressure})

@app.route('/cooleron', methods=['GET'])
def cooler_on():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = subprocess.run(['cgir', 'send', 'cooler_on'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Cooler turned on', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to turn on cooler', 'output': e.stderr.decode()}), 500

@app.route('/heateron', methods=['GET'])
def heater_on():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = subprocess.run(['cgir', 'send', 'heater_on'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Heater turned on', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to turn on heater', 'output': e.stderr.decode()}), 500

@app.route('/tempup', methods=['GET'])
def temp_up():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = subprocess.run(['cgir', 'send', 'temp_up'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Temperature up', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to increase temperature', 'output': e.stderr.decode()}), 500

@app.route('/tempdown', methods=['GET'])
def temp_down():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = subprocess.run(['cgir', 'send', 'temp_down'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Temperature down', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to decrease temperature', 'output': e.stderr.decode()}), 500

@app.route('/turnoff', methods=['GET'])
def turn_off():
    if not check_password():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = subprocess.run(['cgir', 'send', 'turn_off'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'message': 'Conditioner turned off', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to turn off conditioner', 'output': e.stderr.decode()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
