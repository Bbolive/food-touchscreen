from flask import Flask, jsonify
from flask_cors import CORS
from detect import detect_food

app = Flask(__name__)
CORS(app)

TEST_IMAGE = "../frontend/images/test02.jpg"

# ราคาต่อกรัม (ตัวอย่าง)
PRICE_PER_GRAM = {
    "ข้าวมันไก่ต้ม": 0.45,
    "ข้าวมันไก่ทอด": 0.55,
    "ก๋วยเตี๋ยวไก่น่อง": 0.50,
    "default": 0.40
}

def predict_weight_from_area(detections, image_area):
    """
    วิธีที่ 3: Normalize ด้วยขนาดภาพ
    """
    if not detections or image_area == 0:
        return 0

    TOTAL_REFERENCE_WEIGHT = 220  # น้ำหนักอ้างอิง (กรัม)

    total_bbox_area = sum(d["area"] for d in detections)
    normalized_ratio = total_bbox_area / image_area

    weight = normalized_ratio * TOTAL_REFERENCE_WEIGHT

    # จำกัดช่วงน้ำหนักให้สมจริง
    weight = max(150, min(weight, 260))

    return round(weight, 2)

def calculate_price(menu, weight):
    """
    ราคาแบบร้านจริง
    """
    if menu == "ข้าวมันไก่ต้ม":
        if weight < 200:
            return 35
        elif weight < 240:
            return 45
        else:
            return 50

    elif menu == "ข้าวมันไก่ทอด":
        if weight < 200:
            return 40
        elif weight < 240:
            return 50
        else:
            return 55

    return 40

@app.route("/detect", methods=["GET"])
def detect():
    result = detect_food(TEST_IMAGE)

    menu_name = result["menu"]
    detections = result["detections"]
    image_area = result["image_area"]

    if not detections:
        return jsonify({
            "menu": menu_name,
            "weight_gram": 0,
            "price_baht": 0
        })

    weight = predict_weight_from_area(detections, image_area)
    price = calculate_price(menu_name, weight)

    return jsonify({
        "menu": menu_name,
        "weight_gram": weight,
        "price_baht": price,
        "detections": detections
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
