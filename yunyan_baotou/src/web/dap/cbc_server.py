# coding=utf-8
import flask
from flask import Flask, Response
from functools import wraps
import json
from dutil.utility import CJsonEncoder
from dmp.gongan.gz_case_money.moneyCount import *
from dmp.gongan.gz_case_date.predict import ner_predict as ner_predict_date
from dmp.gongan.Entity_name.predict import ner_predict as ner_predict_name


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


@app.route('/gzcase/msum', methods=['POST', 'GET'])
@log_service('计算每个case的涉案金额', ['messageid', 'clientid', 'text'])
def crimin_predict(param=None):
    print(param)
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (
            isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = sum_money(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


@app.route('/gzcase/date', methods=['POST', 'GET'])
@log_service('计算每个case案发时间', ['messageid', 'clientid', 'text'])
def crimin_date(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (
            isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = ner_predict_date(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': [x.get('date') for x in predict_result],
    }
    return result


@app.route('/algor/namextr', methods=['POST', 'GET'])
@log_service('计算每个姓名', ['messageid', 'clientid', 'text'])
def crimin_name(param=None):
    predict_str = param['text']
    encrypt = True if (isinstance(param['encrypt'], bool) and param['encrypt']) or (
            isinstance(param['encrypt'], str) and param['encrypt'].upper() == 'TRUE') else False
    predict_result = ner_predict_name(predict_str, encrypt=encrypt)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': [x.get('per') for x in predict_result],
    }
    return result


if __name__ == "__main__":
    app = flask.Flask(__name__)
    child_sys_id = 'DMP'
    app.run(host='0.0.0.0', debug=True, port=7999, use_reloader=True, threaded=True)
    # app.run(host='0.0.0.0', debug=True)
