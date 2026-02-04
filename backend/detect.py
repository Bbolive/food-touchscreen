from ultralytics import YOLO
import cv2

# โหลดโมเดล
model = YOLO("best.pt")

# ===============================
# กำหนดขนาดภาพ (ต้องตรงกับภาพจริง)
# ===============================
IMG_WIDTH = 640
IMG_HEIGHT = 480

# กฎเมนู
MENU_RULES = {
    "ข้าวมันไก่ต้ม": {
        "ingredients": {"boiled_chicken_blood_jelly", "chicken_rice"}
    },
    "ข้าวมันไก่ทอด": {
        "ingredients": {"fried_chicken", "chicken_rice"}
    },
    "ก๋วยเตี๋ยวไก่น่อง": {
        "ingredients": {"chicken_drumstick", "noodles"}
    }
}

def detect_food(image_path):
    img = cv2.imread(image_path)
    results = model(img, conf=0.4)

    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            conf = round(float(box.conf[0]), 2)

            x1, y1, x2, y2 = box.xyxy[0]
            area = float((x2 - x1) * (y2 - y1))

            detections.append({
                "name": label,
                "confidence": conf,
                "area": round(area, 2)
            })

    print("🔍 RAW DETECT:", detections)

    # ===============================
    # 🧠 รวมวัตถุดิบ → เมนู
    # ===============================
    best_menu = None
    best_score = 0
    best_conf = 0

    for menu, rule in MENU_RULES.items():
        matched = [d for d in detections if d["name"] in rule["ingredients"]]

        if matched:
            score = len(matched)
            avg_conf = sum(d["confidence"] for d in matched) / score

            if score > best_score:
                best_score = score
                best_menu = menu
                best_conf = round(avg_conf, 2)

    if not best_menu:
        best_menu = "ไม่สามารถระบุเมนูได้"
        best_conf = 0.0

    return {
        "menu": best_menu,
        "confidence": best_conf,
        "detections": detections,
        "image_area": IMG_WIDTH * IMG_HEIGHT
    }
