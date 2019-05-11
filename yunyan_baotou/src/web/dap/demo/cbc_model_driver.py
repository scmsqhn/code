# coding=utf-8
import requests
import json
from dmp.store.db import default_sql as Db

def cbc_model_driver():

    headers = {'content-type': 'application/json', "Accept": "application/json"}

    ents = Db.query('select id, name from b_enterprise_info e')
    models = Db.query('select modelid from b_app_model')
    if ents != None or models != None:
        for ent in ents:
            print(ent[0])
            for model in models:
                values = {"user_id": ent[0], "model_id": model[0]}
                r = requests.post('http://localhost:7777/cbc', data=json.dumps(values), headers=headers)
                print(r.text)

if __name__ == "__main__":
    cbc_model_driver()