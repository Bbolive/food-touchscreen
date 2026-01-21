from ultralytics import YOLO
import cv2

# โหลดโมเดล YOLOv8 ที่ได้จาก Roboflow
model = YOLO("best.pt")  # ใส่ path โมเดลที่ export มา

def detect_food(image_path):
    """
    รับ path ของภาพ
    คืนค่าเป็น list ของอาหารและความมั่นใจ
    """
    img = cv2.imread(image_path)
    results = model(img)

    foods = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            foods.append({
                "food": label,
                "confidence": round(conf, 2)
            })
    return foods