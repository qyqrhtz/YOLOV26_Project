from ultralytics import YOLO

model = YOLO("yolo26n.pt")

model.train(
    data="/Users/qyqrhtz/Downloads/Clothing Detection.v1i.yolo26 (1)/data.yaml",
    epochs=30,
    imgsz=640,
    batch=32,              # 先降下来，稳一点
    close_mosaic=10,
    patience=20,
    seed=0,
    device="mps",
    amp=True,            # MPS下建议先关掉
    workers=0,            # 你日志里本来就是0
    optimizer="AdamW",    # 显式指定，避免auto再改
    name="train4_"
)

metrics = model.val(
    data="/Users/qyqrhtz/Downloads/Clothing Detection.v1i.yolo26 (1)/data.yaml",
    split="val"           # 先用val，最稳
)

print("验证集 mAP50-95:", metrics.box.map)
print("完成!")