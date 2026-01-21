from ultralytics import YOLO
import cv2
from collections import defaultdict

model = YOLO("best.pt")

# กฎเมนู
MENU_RULES = {
    "ข้าวมันไก่ต้ม": {
        "ingredients": {"boiled_chicken_blood_jelly", "chicken_rice"},
    },
    "ข้าวมันไก่ทอด": {
        "ingredients": {"fried_chicken", "chicken_rice"},
    },
    "ก๋วยเตี๋ยวไก่น่อง": {
        "ingredients": {"chicken_drumstick", "noodles"},
    },
}

def detect_food(image_path):
    img = cv2.imread(image_path)
    results = model(img)

    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]

            detections.append({
                "name": label,
                "confidence": round(conf, 2)
            })

    print("🔍 DETECTED:", detections)

    # ===============================
    # 🧠 รวมวัตถุดิบ → เดาเมนู
    # ===============================
    detected_names = [d["name"] for d in detections]

    best_menu = None
    best_score = 0
    best_conf = 0

    for menu, rule in MENU_RULES.items():
        matched = [
            d for d in detections
            if d["name"] in rule["ingredients"]
        ]

        if matched:
            score = len(matched)
            avg_conf = sum(d["confidence"] for d in matched) / score

            if score > best_score:
                best_score = score
                best_menu = menu
                best_conf = round(avg_conf, 2)

    if best_menu:
        return [{
            "food": best_menu,
            "confidence": best_conf
        }]

    return [{
        "food": "ไม่สามารถระบุเมนูได้",
        "confidence": 0.0
    }]
