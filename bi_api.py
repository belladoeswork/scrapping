from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        with open('result.json', 'r') as f:
            data = json.load(f)
            return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'message': 'No events data available. Please run the scraper first.'}), 404

if __name__ == "__main__":
    app.run(port=9006)