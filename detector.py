# detector.py
from ultralytics import YOLO
import os
import cv2
import glob

MODEL_PATH = "runs/detect/train4_-9/weights/best.pt"
CURRENT_MODEL_PATH = os.path.normpath(MODEL_PATH)

names = {
    0: "短袖T恤",
    1: "连衣裙",
    2: "短裤?",
    3: "长裤",
    4: "衬衫",
    5: "短裤",
    6: "裙子",
    7: "外套"
}


model = YOLO(CURRENT_MODEL_PATH)


def get_model_path():
    return CURRENT_MODEL_PATH.replace("\\", "/")


def list_available_models():
    candidates = glob.glob("runs/detect/**/weights/*.pt", recursive=True)
    candidates += glob.glob("*.pt")
    normalized = {os.path.normpath(p) for p in candidates if os.path.isfile(p)}
    normalized.add(CURRENT_MODEL_PATH)

    paths = sorted(normalized)
    return [
        {
            "path": p.replace("\\", "/"),
            "is_current": os.path.normpath(p) == CURRENT_MODEL_PATH
        }
        for p in paths
    ]


def set_model_path(model_path):
    global model
    global CURRENT_MODEL_PATH

    normalized_path = os.path.normpath(model_path)
    if not os.path.isfile(normalized_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}")

    model = YOLO(normalized_path)
    CURRENT_MODEL_PATH = normalized_path
    return get_model_path()


def detect_image(image_path):
    results = model.predict(source=image_path, conf=0.25, save=False)
    r = results[0]
    print(type(r.names))
    print(r.names)

    os.makedirs("results", exist_ok=True)
    r.names = names
    plotted = r.plot()

    base_name = os.path.basename(image_path)
    result_path = os.path.join("results", base_name)

    cv2.imwrite(result_path, plotted)

    detections = []
    for box in r.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append({
            "类别": names.get(cls,f"未知类别{cls}"),
            "置信度": round(conf, 3),
            "框": [round(x1), round(y1), round(x2), round(y2)]
        })

    return {
        "原图路径": image_path,
        "检测结果路径": f"http://127.0.0.1:8000/{result_path}",
        "目标数量": len(detections),
        "检测结果": detections
    }
