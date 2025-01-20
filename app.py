from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Secure CORS configuration
CORS(app, resources={
    r"/test": {
        "origins": [
            "http://localhost:5173",  # Development frontend
            "https://us-east-1.console.aws.amazon.com/amplify/apps/d1kze5vw3hqljr/overview"  # Production frontend
        ],
        "methods": ["GET"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600  # Cache preflight requests for 1 hour
    }
}, supports_credentials=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello from a secure EC2 server!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
