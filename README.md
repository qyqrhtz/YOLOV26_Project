# YOLOV26_服装分类检测课程设计Project

基于 YOLO、FastAPI 和 MySQL 的服装目标检测项目，提供图片上传、目标识别、检测记录管理和模型切换能力。

## 功能

- 图片上传与目标检测
- 检测结果图片输出
- 检测记录保存、查询和删除
- 可用模型列表查询与模型切换
- 训练指标与图表读取
- 简单前端页面展示

## 技术栈

- FastAPI
- Ultralytics YOLO
- OpenCV
- PyMySQL
- NumPy

## 项目结构

- `app.py`：FastAPI 应用入口
- `detector.py`：模型加载、切换与推理逻辑
- `record_service.py`、`record_repo.py`：检测记录服务与数据访问
- `db.py`：数据库连接
- `frontend/`：前端页面
- `train.py`：训练脚本
- `requirements.txt`：依赖列表

## 安装与运行

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

默认服务地址：

```text
http://127.0.0.1:8000
```

## 主要接口

- `POST /detect`
- `GET /records`
- `DELETE /records/{record_id}`
- `GET /models`
- `PUT /model`
- `GET /model-metrics`

## 说明

- 项目内保留了模型权重、测试图片和部分结果文件，方便直接复现
- 运行前需要确保 MySQL 中已准备好对应数据库与数据表
