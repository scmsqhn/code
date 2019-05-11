# coding=utf-8
import flask
import json
from functools import wraps
from dmp.gongan.gz_crim_loc_classify.gonganpred import criminalpredict
from dutil.log import logger
from dutil.utility import CJsonEncoder
import requests
from requests.exceptions import ConnectionError
import re

app = flask.Flask(__name__)
child_sys_id = 'NER'


def log_event(param, event, interface_name, log_level='info'):
    log_message = {'child_sys_id': child_sys_id, 'host_no': flask.request.remote_addr,
                   'monitor_name': '{0}计算'.format(interface_name),
                   'business_no': param['messageid'] if 'messageid' in param else None,
                   'business_name': '{0}接口'.format(interface_name), }
    if log_level == 'error':
        logger.error('{0}{1}'.format(interface_name, event), log_message)
    else:
        logger.info('{0}{1}'.format(interface_name, event), log_message)


def param_error(param, interface_name):
    log_event(param, '接口参数错误', interface_name, 'error')
    result = {
        'messageid': param['messageid'] if 'messageid' in param else None,
        'clientid': param['clientid'] if 'clientid' in param else None,
        'resultcode': '010'
    }
    return result


def heartbeat_test(param, interface_name):
    log_event(param, '接口心跳测试', interface_name)
    result = {
        'messageid': param['messageid'] if 'messageid' in param else None,
        'clientid': param['clientid'] if 'clientid' in param else None,
        'resultcode': '001'
    }
    return result


def log_service(interface_name, key_params=['user_id', 'model_id', 'messageid', 'clientid']):
    def decorator(func):
        @wraps(func)
        def wrapped():
            logger.debug(flask.request.data)
            param = json.loads(flask.request.data.decode())
            if 'action' in param and param['action'] == 'test':
                result = heartbeat_test(param, interface_name)
                return json.dumps(result, ensure_ascii=False)
            for key_param in key_params:
                if key_param not in param:
                    result = param_error(param, interface_name)
                    return json.dumps(result, ensure_ascii=False)
            log_event(param, '计算开始...', interface_name)
            logger.debug(json.dumps(param, indent=2, ensure_ascii=False))
            result = func(param)
            log_event(param, '计算完成', interface_name)
            return json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)

        return wrapped

    return decorator


@app.route('/all/predict', methods=['POST', 'GET'])
@log_service('predict location', ['messageid', 'clientid','encrypt','text'])
def predict(param=None):
    predict_str = param['text']
    messageid = param['messageid']
    cid = param['clientid']
    encrypt = param['encrypt']
    headers = {'content-type': 'application/json', "Accept": "application/json"}
    resultcode = "000"
    data = {"messageid": messageid,
            "clientid": cid,
            "text": predict_str,
            "encrypt":encrypt
            }
    ExMessage = ""
    try:
        # get goods
        url = "http://localhost:7788/algor/ner"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        goods = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = "涉案金额服务获取异常" + " "
    try:
        #get location
        url = "http://localhost:7789/loc/predict"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        location = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "作案部位预测服务异常" + " "
    try:
        #get caseType
        url = "http://localhost:7790/type/predict"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        casetype = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "案件类型预测服务异常" + " "
    try:
        #get caseMethod
        url = "http://localhost:7791/method/predict"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        method = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "作案手段预测服务异常" + " "
    try:
        # get money_sum
        url = "http://localhost:7777/gzcase/msum"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        money_sum = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "涉案金额服务获取异常" + " "
    try:
        #get caseLocation
        url = "http://localhost:7794/method/caselocation"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        # print('==================')
        # print(res)
        # print('==================')
        caseloc = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "作案caselocation预测服务异常" + " "
    try:
        # get case_date
        url = "http://localhost:7777/gzcase/date"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        case_date = json.loads(res.text)['result']
    except ConnectionError as ce:
        ExMessage = ExMessage + "案发时间服务获取异常" + " "
    if ExMessage:
        result = {
            'messageid': messageid,
            'clientid': cid,
            'resultcode': '011',
            'result': ExMessage
        }
        return result
    else:
        result = {
            'messageid': messageid,
            'clientid': cid,
            'resultcode': '000',
            'result': {"goods": goods, "location": location, "caseType": casetype, "caseMethod": method,"caseSum":money_sum, "caseLoc":caseloc,"case_date":case_date},
        }
        return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7792, use_reloader=True, threaded=True)
    # remote ip:port    113.204.229.74:18087
