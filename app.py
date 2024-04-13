from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Event Scraper API!'})

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        with open('result.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'message': 'No events data available. Please run the scraper first.'}), 404

if __name__ == "__main__":
    run_spider('event_spider')
    app.run(debug=True, port=9000)
    
