from main import engine, ApiInfo
from sqlmodel import Session, select
import json

if __name__ == "__main__":
    with Session(engine) as session:
        statement = select(ApiInfo).limit(500)
        result = session.exec(statement)

        json_list = []

        for record in result:
            json_list.append(record.api_info_json)
        
        with open('json_list', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_list))
