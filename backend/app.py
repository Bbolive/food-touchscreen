from flask import Flask, jsonify
from flask_cors import CORS
from detect import detect_food

app = Flask(__name__)
CORS(app)

TEST_IMAGE = "../frontend/images/test02.jpg"

@app.route("/detect", methods=["GET"])
def detect():
    results = detect_food(TEST_IMAGE)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
