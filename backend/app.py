from flask import Flask, jsonify
from flask_cors import CORS
from detect import detect_food

app = Flask(__name__)
CORS(app)

# ตัวอย่างภาพสำหรับทดสอบ
TEST_IMAGE = "../frontend/test02.jpg"

@app.route("/detect", methods=["GET"])
def detect():
    results = detect_food(TEST_IMAGE)
    # ถ้าไม่มีผลลัพธ์ คืนค่า "No food detected"
    if not results:
        return jsonify({"message": "No food detected"})
    return jsonify(results)

if __name__ == "__main__":
    # รัน server ให้เว็บเรียกได้จากเครื่องอื่น
    app.run(host="0.0.0.0", port=5000, debug=True)