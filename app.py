from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Restrict CORS to API Gateway
CORS(app, resources={r"/*": {"origins": "https://x91quab646.execute-api.us-east-1.amazonaws.com"}})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello from a secure EC2 server!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
