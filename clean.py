import os

folder = "uploads"
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("删除成功")
    else:
        print("文件不存在")
folder = "results"
for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("删除成功")
    else:
        print("文件不存在")

