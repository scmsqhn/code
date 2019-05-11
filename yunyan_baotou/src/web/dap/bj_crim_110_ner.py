# coding=utf-8

#from gevent.pywsgi import WSGIServer
import datetime
import flask
from flask import Flask, Response
import json
from functools import wraps
import sys
sys.path.append('..')
from dutil.log import logger
from dutil.utility import CJsonEncoder, decrypt_sentences
from dmp.gongan.storm_crim_classify.extcode import digital_info_extract as dgex
from dmp.gongan.bj_crim_ner_suspect_character.predict_ner import predict_ner_height, predict_ner_stature, \
    predict_ner_nation, predict_ner_sex, predict_ner_age, \
    predict_ner_accent, predict_ner_character, predict_ner_hairstyle


child_sys_id = 'BJ110'


class IbaResponse(Response):
    default_mimetype = 'application/json'


class IbaFlask(Flask):
    response_class = IbaResponse


app = IbaFlask(__name__)


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


@app.route('/predict/110/phoneNum', methods=['POST', 'GET'])
@log_service('北京110手机', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_phone(param=None):
    print("view function of predict_phone start:", datetime.datetime.now())
    predict_str = param['text']
    encrypt = param['encrypt']
    print("decrypt_sentences:", datetime.datetime.now())
    predict_str = decrypt_sentences(predict_str, encrypt)
    print("extract_digital_spec:", datetime.datetime.now())
    predict_result = dgex.extract_digital_spec("phoneNum", predict_str)
    print("return of extract_digital_spec:", datetime.datetime.now())
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    print("final request view function of predict_phone end:", datetime.datetime.now())
    return result


@app.route('/predict/110/identifier', methods=['POST', 'GET'])
@log_service('北京110身份证', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_id(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("identifier", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/carinfo', methods=['POST', 'GET'])
@log_service('北京110车辆', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_car(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("carinfo", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/weixin', methods=['POST', 'GET'])
@log_service('北京110微信', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_wx(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("wx", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/qq', methods=['POST', 'GET'])
@log_service('北京110QQ', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_qq(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("qq", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/weibo', methods=['POST', 'GET'])
@log_service('北京110微博', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_weibo(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("weibo", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/creditCard', methods=['POST', 'GET'])
@log_service('北京110分类', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_creditcard(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("creditCard", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/momo', methods=['POST', 'GET'])
@log_service('默默', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_momo(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("momo", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/nickname', methods=['POST', 'GET'])
@log_service('外号', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_nickname(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("nickname", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/website', methods=['POST', 'GET'])
@log_service('网址', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_website(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("web", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/mail', methods=['POST', 'GET'])
@log_service('网址', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_mail(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("mail", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/qqname', methods=['POST', 'GET'])
@log_service('网址', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_qqname(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("qqname", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/wxname', methods=['POST', 'GET'])
@log_service('网址', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_wxname(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = dgex.extract_digital_spec("wxname", predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


########################


@app.route('/predict/110/height', methods=['POST', 'GET'])
@log_service('嫌疑人身高', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_height(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_height(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/stature', methods=['POST', 'GET'])
@log_service('嫌疑人体型', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_stature(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_stature(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/nation', methods=['POST', 'GET'])
@log_service('嫌疑人民族', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_nation(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_nation(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/sex', methods=['POST', 'GET'])
@log_service('嫌疑人性别', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_sex(param=None):
    predict_str = param['text']
    print('嫌疑人性别')
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_sex(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/age', methods=['POST', 'GET'])
@log_service('嫌疑人年龄', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_age(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_age(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/accent', methods=['POST', 'GET'])
@log_service('嫌疑人口音', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_accent(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_accent(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/hairstyle', methods=['POST', 'GET'])
@log_service('嫌疑人发型', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_hairstyle(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_hairstyle(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/predict/110/character', methods=['POST', 'GET'])
@log_service('嫌疑人特殊特征', ['messageid', 'clientid', 'encrypt', 'text'])
def predict_character(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    predict_str = decrypt_sentences(predict_str, encrypt)
    predict_result = predict_ner_character(predict_str)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


if __name__ == "__main__":
    #http_server = WSGIServer(('0.0.0.0', 9999),app)  #替代app.run()方法
    #http_server.serve_forever()
    app.run(host='0.0.0.0', debug=True, port=27719, use_reloader=True, threaded=True)

