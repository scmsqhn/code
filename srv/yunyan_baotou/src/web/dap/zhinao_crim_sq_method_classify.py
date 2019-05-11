# coding=utf-8
import flask
from flask import Flask, Response
import json
from functools import wraps
from dutil.log import logger
from dutil.utility import CJsonEncoder, decrypt_sentences
# TODO 包名
from dmp.gongan.zhinao_crim_sq_method_classify.gonganpred import predict as method_predict


child_sys_id = 'Zhinao'


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
            print(param)
            print(flask.request.url)
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


# TODO 修改URI
@app.route('/classify/method', methods=['POST', 'GET'])
@log_service('Zhinao', ['messageid', 'clientid', 'encrypt', 'text'])
def predict(param=None):
    predict_str = param['text']
    encrypt = param['encrypt']

    predict_str = decrypt_sentences(predict_str, encrypt)

    predict_result = method_predict(predict_str, True)
    result = {
        'messageid': param['messageid'],
        'clientid': param['clientid'],
        'resultcode': '000',
        'result': predict_result,
    }
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999) #, debug=True, use_reloader=True, threaded=True)
    """
    a = [
            '11年8月4日12时许，高元顶（男，汉族，高中文化，1972年11月11日，户籍地址：四川省古蔺县双沙镇德安村二组１８号，身份证号码：510525195601057772，现住：贵阳市云岩区野鸭塘，联系电话：15285914535）报称在贵阳市云岩区浣纱路花香酒店门口的人行天桥上，被人以走路发生碰撞为由，抢走现金人民币：130元。',
            '12年02月16日16时50分许，我所接市局110指令，市西路商业街6号地，被抢夺一部手机。接警后值班民警曾祥和叶迪海立即组织警力赶往现场进行调查，经受害人高娟(女、汉族、1983年03月13日生、本科文化程度，身份证号：520103198203131223，户籍所在地：贵阳市云岩区翠屏巷59号附8号；现住：贵阳市云岩区翠屏巷59号附8号，联系电话：6766032),报称其在贵阳市云岩区市西路商业街六号，被一名男子抢夺走一个苹果4代黑色手机，购价：5880元 购于：2011年4月左右，黑色，被抢手机号码是：18685008110，串号不详。',
    ]
    print(method_predict(a))
    """


