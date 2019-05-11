# coding=utf-8
import flask
from flask import Flask, Response
import json
from functools import wraps
#from dmp.gongan.gz_case_detail.caseDetails import user_idcard, phone_sn,  phone_number, phone_card, plate_number, mac_addr, vehicle_sn, engine_sn, case_location
from dmp.gongan.storm_crim_classify import extcode
from dmp.gongan.storm_crim_classify.extcode import digital_info_extract
from dutil.log import logger
from dutil.utility import CJsonEncoder
# from dmp.gongan.gz_case_location.regex_ner import criminalpredict
#from dmp.gongan.gz_case_address.predict import ner_predict as addr_ner_predict
from dutil.utility import CJsonEncoder, decrypt_sentences

print("\n> marker")
class IbaResponse(Response):
    default_mimetype = 'application/json'

class IbaFlask(Flask):
    response_class = IbaResponse

app = IbaFlask(__name__)

child_sys_id = 'NER'

print("\n> marker")
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


print("\n> marker")
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

namedict = {}
namedict['criminalidentifier'] = 'criminal_identifier'
namedict['criminalphone'] = 'criminal_phone'
namedict['criminalwx'] = 'criminal_wx'
namedict['criminalqq'] = 'criminal_qq'

@app.route('/test', methods=['POST', 'GET'])
@log_service('test code', ['messageid','clientid','encrypt', 'text', 'funcname'])
def test(param=None):
    result = {
        'messageid': 'messageid',
        'clientid': 'clientid',
        'resultcode': '000',
        'result': "yes i am working know",
        }
    return result

print("\n> marker")
@app.route('/ner', methods=['POST', 'GET'])
@log_service('ner code', ['messageid','clientid','encrypt', 'text', 'funcname'])
def extract_phone_num(param=None):
    print('extract_phone_num')
    # this port is ner for num and char like identifier phonenum ws qq ans do on
    # ! but no inclued the "total interface" to get all the above we mentioned
    predict_str = param['text']
    #predict_str = decrypt_sentences(predict_str, encrypt)
    #encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    funcname = ""
    if param['funcname'] in namedict.keys():
      funcname = namedict[param['funcname']]
    else:
      funcname = param['funcname']
    print("Sorry, there is no the key in the dict.")  
    predict_result = digital_info_extract.extract_digital_spec(funcname, predict_str, False)#encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result

print("\n> marker")
if __name__ == "__main__":
    print("\n> marker")
    app.run(host='0.0.0.0', debug=True, port=7794, use_reloader=True, threaded=True)
    print("\n>app is running")
