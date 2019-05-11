# coding=utf-8
import flask
from flask import Flask, Response
import json
from functools import wraps
from dutil.log import logger
from dutil.utility import CJsonEncoder, decrypt_sentences
from dmp.gongan.zhinao_vehicle_theft_case_classify.gonganpred import criminalpredict


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


def log_service(interface_name, key_params=['user_id', 'model_id', 'messageid', 'clientid', 'debug']):
    def decorator(func):
        @wraps(func)
        def wrapped():
            logger.debug(flask.request.data)
            param = json.loads(flask.request.data.decode())
            print(param)
            print(flask.request.url)
            if 'action' in param and param['action'] == 'test':
                result = heartbeat_test(param, interface_name)
                return json.dumps(result, ensure_ascii=False)
            for key_param in key_params:
                if key_param not in param and key_param != 'debug':
                    result = param_error(param, interface_name)
                    return json.dumps(result, ensure_ascii=False)
            log_event(param, '计算开始...', interface_name)
            logger.debug(json.dumps(param, indent=2, ensure_ascii=False))
            result = func(param)
            log_event(param, '计算完成', interface_name)
            return json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)

        return wrapped

    return decorator


@app.route('/zhinao/vehicle/case-classify', methods=['POST', 'GET'])
@log_service('智脑3涉车盗窃.案由分类', ['messageid', 'clientid', 'encrypt', 'text'])
def predict(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']
    try:
        debug = param['debug']
    except KeyError as e:
        debug = False

    predict_str = decrypt_sentences(predict_str, encrypt)

    predict_result = criminalpredict(predict_str, debug)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    print(result)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=19999) #, debug=True) #, use_reloader=True, threaded=True)


