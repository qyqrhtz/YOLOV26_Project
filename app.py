from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from detector import detect_image, get_model_path, list_available_models, set_model_path
from record_service import save_detection_record, list_detection_records, remove_detection_record

import csv
import os
import time
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/results", StaticFiles(directory="results"), name="results")
app.mount("/runs", StaticFiles(directory="runs"), name="runs")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def root():
    return {"message": "API 已启动"}


class ModelUpdateRequest(BaseModel):
    model_path: str

@app.post("/detect")
async def detect_api(file: UploadFile = File(...)):
    os.makedirs("uploads",exist_ok=True)

    filename = f"{int(time.time())}_{file.filename}"
    file_path = os.path.join("uploads",filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = detect_image(file_path)
    save_detection_record(result)

    return result


@app.post("/upload_test")
async def upload_test(file: UploadFile = File(...)):
    print(file.filename)
    return {"filename": file.filename,
            "msg": "上传成功"}

@app.get("/records")
def get_records():
    return list_detection_records()

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    remove_detection_record(record_id)
    return {"message": "删除成功"}


@app.get("/model")
def get_current_model():
    return {"model_path": get_model_path()}


@app.get("/models")
def get_models():
    return {
        "current_model": get_model_path(),
        "models": list_available_models()
    }


@app.put("/model")
def update_model(payload: ModelUpdateRequest):
    try:
        new_model_path = set_model_path(payload.model_path)
        return {"message": "模型切换成功", "model_path": new_model_path}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"模型加载失败: {str(e)}")


def _read_training_metrics(csv_path: str):
    if not os.path.isfile(csv_path):
        return {}

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            return {}
        last = rows[-1]
        keys = [
            "metrics/precision(B)",
            "metrics/recall(B)",
            "metrics/mAP50(B)",
            "metrics/mAP50-95(B)",
            "fitness"
        ]
        metrics = {}
        for key in keys:
            val = last.get(key)
            if val in (None, ""):
                continue
            try:
                metrics[key] = round(float(val), 4)
            except ValueError:
                continue
        return metrics
    except Exception:
        return {}


@app.get("/model-metrics")
def get_model_metrics(model_path: str = Query(default="")):
    model_items = []
    current_model = get_model_path()
    target_model = os.path.normpath(model_path) if model_path else ""

    for item in list_available_models():
        model_file_path = os.path.normpath(item["path"])
        if target_model and os.path.normpath(model_file_path) != target_model:
            continue

        weights_dir = os.path.dirname(model_file_path)
        if os.path.basename(weights_dir) != "weights":
            continue

        train_dir = os.path.dirname(weights_dir)
        if not os.path.isdir(train_dir):
            continue

        charts = {}
        chart_files = {
            "results": "results.png",
            "pr_curve": "BoxPR_curve.png",
            "f1_curve": "BoxF1_curve.png",
            "confusion_matrix": "confusion_matrix.png"
        }
        for key, filename in chart_files.items():
            fp = os.path.join(train_dir, filename)
            if os.path.isfile(fp):
                charts[key] = "http://127.0.0.1:8000/runs/" + os.path.relpath(fp, "runs").replace("\\", "/")

        metrics = _read_training_metrics(os.path.join(train_dir, "results.csv"))
        model_items.append({
            "model_path": model_file_path.replace("\\", "/"),
            "train_dir": train_dir.replace("\\", "/"),
            "is_current": os.path.normpath(model_file_path) == os.path.normpath(current_model),
            "metrics": metrics,
            "charts": charts
        })

    return {
        "current_model": current_model,
        "models": model_items
    }
