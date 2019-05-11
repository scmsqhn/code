# coding=utf-8
import flask
from flask import Flask, Response
from flask import request
import json
from dmp.gongan.gz_case_date.predict import ner_predict

child_sys_id = 'NER'

class IbaResponse(Response):
    default_mimetype = 'application/json'


class IbaFlask(Flask):
    response_class = IbaResponse


app = IbaFlask(__name__)


@app.route('/predict/110/date', methods=['POST', 'GET'])
def predict():
    param = request.get_json()
    print(type(param), param)
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = ner_predict(predict_str,encrypt=encrypt)
    print('==='*10, '\n', predict_result)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': [x.get('date') for x in predict_result],
    }
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7692, use_reloader=True, threaded=True)
