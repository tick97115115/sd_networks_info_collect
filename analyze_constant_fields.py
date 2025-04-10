from typing import List, Dict, Any
from collections import defaultdict
from sqlmodel import Session, select
from main import ApiInfo, engine
from sqlalchemy.engine import Engine
import pydash as _

def dict_paths_generator(data, parent_key='', separator='.'):
    for key, value in data.items():
        current_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            yield from dict_paths_generator(value, current_key, separator)
        else:
            yield current_key

# 示例
# print(list(dict_paths_generator({'a':1, 'b': {'c': 2, 'd': 3, 'e': {'f': 4}}})))

def find_every_constant_properties():
    """
    查找数据库中所有的 API 信息，并提取每个 API 信息中的所有常量属性
    """
    with Session(engine) as session:
        statement = select(ApiInfo)
        results = session.exec(statement)

        first_time = True
        all_constant_properties: List[str] = []

        for item in results:
            if first_time:
                first_time = False
                all_constant_properties = list(dict_paths_generator(item.api_info_json))
            else:
                all_constant_properties = _.intersection(
                    all_constant_properties,
                    list(dict_paths_generator(item.api_info_json))
                )
        
        print("所有 API 信息中的常量属性:")
        for prop in all_constant_properties:
            print(prop)
        
        open("constant_properties.txt", "w").write("\n".join(all_constant_properties))
        print("常量属性已写入 constant_properties.txt 文件中。")
        return all_constant_properties

def find_every_modelVersion_constant_fields():
    """
    查找数据库中所有的 API 信息，并提取每个 API 信息中的所有常量属性
    """
    with Session(engine) as session:
        statement = select(ApiInfo)
        results = session.exec(statement)

        first_time = True
        all_constant_fields: List[str] = []

        for item in results:
            for modelVersion in item.api_info_json.get('modelVersions', []):
                if first_time:
                    first_time = False
                    all_constant_fields = list(dict_paths_generator(modelVersion))
                else:
                    all_constant_fields = _.intersection(
                        all_constant_fields,
                        list(dict_paths_generator(modelVersion))
                    )
            # if first_time:
            #     first_time = False
            #     all_constant_fields = list(dict_paths_generator(item.api_info_json))
            # else:
            #     all_constant_fields = _.intersection(
            #         all_constant_fields,
            #         list(dict_paths_generator(item.api_info_json))
            #     )
        
        print("所有 ModelVersion 信息中的常量属性:")
        for prop in all_constant_fields:
            print(prop)
        
        open("modelVersion_constant_properties.txt", "w").write("\n".join(all_constant_fields))
        print("常量属性已写入 modelVersion_constant_properties.txt 文件中。")
        return all_constant_fields

def find_every_modelVersion_files_constant_fields_2():
    """
    查找数据库中所有的 API 信息，并提取每个 API 信息中的所有常量属性
    """
    with Session(engine) as session:
        statement = select(ApiInfo)
        results = session.exec(statement)

        first_time = True
        all_constant_fields: List[str] = []

        for item in results:
            for modelVersion in item.api_info_json.get('modelVersions', []):
                # if first_time:
                #     first_time = False
                #     all_constant_fields = list(dict_paths_generator(modelVersion))
                # else:
                #     all_constant_fields = _.intersection(
                #         all_constant_fields,
                #         list(dict_paths_generator(modelVersion))
                #     )
                for file in modelVersion.get('files', []):
                    if first_time:
                        first_time = False
                        all_constant_fields = list(dict_paths_generator(file))
                    else:
                        all_constant_fields = _.intersection(
                            all_constant_fields,
                            list(dict_paths_generator(file))
                        )
        
        print("所有 ModelVersion.files 信息中的常量属性:")
        for prop in all_constant_fields:
            print(prop)
        
        open("modelVersion_files_constant_properties.txt", "w").write("\n".join(all_constant_fields))
        print("常量属性已写入 modelVersion_files_constant_properties.txt 文件中。")
        return all_constant_fields

def find_every_modelVersion_images_constant_fields_2():
    """
    查找数据库中所有的 API 信息，并提取每个 API 信息中的所有常量属性
    """
    with Session(engine) as session:
        statement = select(ApiInfo)
        results = session.exec(statement)

        first_time = True
        all_constant_fields: List[str] = []

        for item in results:
            for modelVersion in item.api_info_json.get('modelVersions', []):
                # if first_time:
                #     first_time = False
                #     all_constant_fields = list(dict_paths_generator(modelVersion))
                # else:
                #     all_constant_fields = _.intersection(
                #         all_constant_fields,
                #         list(dict_paths_generator(modelVersion))
                #     )
                for image in modelVersion.get('images', []):
                    if first_time:
                        first_time = False
                        all_constant_fields = list(dict_paths_generator(image))
                    else:
                        all_constant_fields = _.intersection(
                            all_constant_fields,
                            list(dict_paths_generator(image))
                        )
        
        print("所有 ModelVersion.images 信息中的常量属性:")
        for prop in all_constant_fields:
            print(prop)
        
        open("modelVersion_images_constant_properties.txt", "w").write("\n".join(all_constant_fields))
        print("常量属性已写入 modelVersion_images_constant_properties.txt 文件中。")
        return all_constant_fields

if __name__ == "__main__":
    # find_every_constant_properties()
    find_every_modelVersion_constant_fields()
    find_every_modelVersion_files_constant_fields_2()
    find_every_modelVersion_images_constant_fields_2()