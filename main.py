from pathlib import Path
from sqlalchemy import Column
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, JSON
import os
import json

class ApiInfo(SQLModel, table=True):
    """
    数据库模型类，表示 API 信息
    """
    id: int | None = Field(default=None, primary_key=True)
    api_info_json: dict = Field(sa_column=Column(JSON) ,default_factory=dict)
    path: str
    folder: str
    extracted_api_info: dict | None = Field(sa_column=Column(JSON) ,default_factory=dict)

sqlite_db_path = Path(__file__).parent / "sd-networks-info-collect.db"

engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
SQLModel.metadata.create_all(engine)

def load_json_file(file_path):
    """
    加载并解析 JSON 文件，返回解析后的字典
    
    Args:
        file_path (str): JSON 文件的路径
        
    Returns:
        dict: 解析后的 JSON 数据
        
    Raises:
        FileNotFoundError: 如果文件不存在
        json.JSONDecodeError: 如果 JSON 格式无效
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON 解析错误: {str(e)}", e.doc, e.pos)

def replace_api_info_suffix(filename: str) -> str:
    """
    将字符串结尾的 '.api_info.json' 替换为 '.json'
    如果字符串不是以 '.api_info.json' 结尾，则返回原字符串
    
    :param filename: 要处理的字符串（通常是文件名或路径）
    :return: 处理后的字符串
    """
    suffix = '.api_info.json'
    if filename.endswith(suffix):
        return filename[:-len(suffix)] + '.json'
    return filename

def find_api_info_files(root_dir: str):
    """
    递归查找文件夹中所有以 'api_info.json' 结尾的文件，并逐个将它们解析并存储到数据库中
    
    :param root_dir: 要搜索的根目录路径
    """
    
    # 遍历根目录下的所有文件和子目录
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # 检查文件名是否以 'api_info.json' 结尾
            if file.endswith('.api_info.json'):
                # 获取文件的绝对路径并添加到数据库中
                with Session(engine) as session:
                    # api_info = ApiInfo(api_info_json_path=os.path.abspath(os.path.join(root, file)))
                    # session.add(api_info)
                    # session.commit()
                    file_path = os.path.abspath(os.path.join(root, file))
                    api_info_json = load_json_file(file_path)
                    record = ApiInfo(api_info_json=api_info_json, path=file_path, folder=str(Path(file_path).parent.absolute()))
                    # 尝试定位简化后的json文件
                    simplified_file_path = replace_api_info_suffix(file_path)
                    if os.path.exists(simplified_file_path):
                        extracted_api_info_json = load_json_file(simplified_file_path)
                        record.extracted_api_info = extracted_api_info_json
                    else:
                        print(f"简化后的 JSON 文件未找到: {simplified_file_path}")
                        record.extracted_api_info = None
                    session.add(record)
                    session.commit()

if __name__ == "__main__":
    find_api_info_files(r"D:\AI_Drawer\webui_forge\webui\models\Lora")
