# coding=utf-8
import flask
import sys
from flask import Flask, Response
import json
import requests
from functools import wraps
from dutil.log import logger
from dutil.utility import CJsonEncoder, decrypt_sentences
import os
CURPATH = os.path.dirname(os.path.realpath(__file__))
PARPATH = os.path.dirname(CURPATH)
sys.path.append(os.path.join(PARPATH, "dmp/gongan/address_formula"))
import dmp.gongan.address_formula
sys.path.extend(dmp.gongan.address_formula.__path__)
import address_predict
print(sys.path[-1])
print(CURPATH,PARPATH)
sys.path.append(PARPATH)
sys.path.append(CURPATH)

class IbaResponse(Response):
    default_mimetype = 'application/json'

class IbaFlask(Flask):
    response_class = IbaResponse

app = IbaFlask(__name__)

child_sys_id = 'ADD_FORMULA'

eval_ins = address_predict.Eval_Ner_Add()

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

@app.route('/normalization/addr-normal', methods=['POST', 'GET'])
@log_service('addr-normal', ['messageid', 'clientid', 'encrypt', 'text'])
def addr_formula(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    # url = "http://localhost:7799/method/addrclassify"
    # headers = {'content-type': 'application/json', "Accept": "application/json"}
    # res = requests.post(url, data=param, headers=headers)
    # caseloc_seg = json.loads(res.text)['result']
    #predict_result = criminalpredict_class_address(predict_str, encrypt)
    predict_result = eval_ins.predict_sent(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7943, use_reloader=True, threaded=True)

