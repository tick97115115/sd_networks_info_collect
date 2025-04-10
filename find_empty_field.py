from main import engine, ApiInfo
from sqlmodel import Session, select
import pydash as _

def find_empty_field():
    """
    查找数据库中所有的 API 信息，并提取每个 API 信息中的所有常量属性
    """
    with Session(engine) as session:
        statement = select(ApiInfo)
        results = session.exec(statement)

        empty_fields = []

        for item in results:
            if not _.has(item.api_info_json, 'modelVersions.0.id'):
                empty_fields.append(item.path)
                print(f"文件 {item.path} 中的 modelVersions.0.id 为空")

        print("API 信息 JSON 为空的文件路径:")
        for path in empty_fields:
            print(path)
        
        open("empty_api_info.txt", "w").write("\n".join(empty_fields))
        print("空的 API 信息 JSON 文件路径已写入 empty_api_info.txt 文件中。")
        return empty_fields

if __name__ == "__main__":
    find_empty_field()