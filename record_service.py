from record_repo import insert_record,get_all_records
from record_repo import delete_record_by_id
import json

def save_detection_record(result: dict):
    print("===== 看 result 整体 =====")
    print(result)
    print(type(result))

    print("===== 看 result['检测结果'] =====")
    print(result["检测结果"])
    print(type(result["检测结果"]))

    print("===== 看 result['检测结果'][0] =====")
    print(result["检测结果"][0])
    print(type(result["检测结果"][0]))

    print("===== json.dumps 后 =====")
    result_json = json.dumps(result["检测结果"], ensure_ascii=False)
    print(result_json)
    print(type(result_json))

    record = {
        "source_image": result["原图路径"],
        "result_image": result["检测结果路径"],
        "target_count": result["目标数量"],
        "result_json": json.dumps(result["检测结果"], ensure_ascii=False)
    }

    insert_record(record)

def list_detection_records():
    return get_all_records()
def remove_detection_record(record_id: int):
    delete_record_by_id(record_id)