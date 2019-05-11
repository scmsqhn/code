# coding=utf-8
import flask
from flask import Flask, Response
import json
from functools import wraps
from dmp.gongan.gz_case_detail.caseDetails import user_idcard, phone_sn,  phone_number, phone_card, plate_number, mac_addr, vehicle_sn, engine_sn, case_location
# from dmp.gongan.storm_crim_classify import extcode
from dmp.gongan.storm_crim_classify.extcode import *
from dmp.gongan.storm_crim_classify.extcode import digital_info_extract
from dutil.log import logger
from dutil.utility import CJsonEncoder
# from dmp.gongan.gz_case_location.regex_ner import criminalpredict
#from dmp.gongan.gz_case_address.predict import ner_predict as addr_ner_predict
from dutil.utility import CJsonEncoder, decrypt_sentences

class IbaResponse(Response):
    default_mimetype = 'application/json'

class IbaFlask(Flask):
    response_class = IbaResponse

app = IbaFlask(__name__)

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

def log_service_funcname(interface_name, key_params=['user_id', 'model_id', 'messageid', 'clientid']):
    def decorator(func):
        @wraps(func)
        def wrapped(funcname):
            print("\n>>>>funcname", funcname)
            print(json.loads(flask.request.data.decode()))
            logger.debug(flask.request.data)
            param = json.loads(flask.request.data.decode())
            print("\n>>>>param", param)
            if 'action' in param and param['action'] == 'test':
                result = heartbeat_test(param, interface_name)
                return json.dumps(result, ensure_ascii=False)
            for key_param in key_params:
                if key_param not in param:
                    print("key_param error")
                    print(key_param)
                    result = param_error(param, interface_name)
                    return json.dumps(result, ensure_ascii=False)
            log_event(param, '计算开始...', interface_name)
            logger.debug(json.dumps(param, indent=2, ensure_ascii=False))
            result = func(param, funcname)
            log_event(param, '计算完成', interface_name)
            return json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)
        return wrapped
    return decorator

def log_service(interface_name, key_params=['user_id', 'model_id', 'messageid', 'clientid']):
    def decorator(func):
        @wraps(func)
        def wrapped():
            print(json.loads(flask.request.data.decode()))
            logger.debug(flask.request.data)
            param = json.loads(flask.request.data.decode())
            print(param)
            if 'action' in param and param['action'] == 'test':
                result = heartbeat_test(param, interface_name)
                return json.dumps(result, ensure_ascii=False)
            for key_param in key_params:
                if key_param not in param:
                    print("key_param error")
                    print(key_param)
                    result = param_error(param, interface_name)
                    return json.dumps(result, ensure_ascii=False)
            log_event(param, '计算开始...', interface_name)
            logger.debug(json.dumps(param, indent=2, ensure_ascii=False))
            result = func(param)
            log_event(param, '计算完成', interface_name)
            return json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)

        return wrapped

    return decorator

@app.route('/ner/<funcname>', methods=['POST', 'GET'])
@log_service_funcname('ner code', ['messageid','clientid','encrypt', 'text'])
def extract_phone_num(param=None, funcname=None):
    # this port is ner for num and char like identifier phonenum ws qq ans do on
    # ! but no inclued the "total interface" to get all the above we mentioned
    predict_str = param['text']
    #predict_str = decrypt_sentences(predict_str, encrypt)
    #encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = digital_info_extract.extract_digital_spec(funcname, predict_str, False)#encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result

@app.route('/method/idcard', methods=['POST', 'GET'])
@log_service('报案人身份证提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_idcard(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = user_idcard(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/simcard', methods=['POST', 'GET'])
@log_service('丢失手机卡号提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_simcard(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = phone_card(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result



@app.route('/method/phonesn', methods=['POST', 'GET'])
@log_service('丢失手机串号提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_phone_sn(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = phone_sn(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/vehiclesn', methods=['POST', 'GET'])
@log_service('车架号提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_vehicle_sn(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = vehicle_sn(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/enginesn', methods=['POST', 'GET'])
@log_service('发动机/电机号提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_engine_sn(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = engine_sn(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/platenum', methods=['POST', 'GET'])
@log_service('车牌号提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_plate_num(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = plate_number(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/macaddr', methods=['POST', 'GET'])
@log_service('电脑mac地址', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_macaddr(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = mac_addr(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/method/caselocation', methods=['POST', 'GET'])
@log_service('案发位置提取', ['messageid', 'clientid', 'encrypt', 'text'])
def extract_location(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = addr_ner_predict(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7794, use_reloader=True, threaded=True)
