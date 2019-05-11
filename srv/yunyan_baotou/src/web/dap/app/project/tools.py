import json
from .iba_exception import *
from dutil.pycrypt import prpcrypt
from dutil.utility import get_config


# def predict(diagram, predict_func):
#     # TODO
#     plaint_text = decrypt_sentences(diagram['text'], diagram['encrypt'])
#     result = predict_func(plaint_text)
#     result = {
#         'messageid': diagram['messageid'],
#         'clientid': diagram['clientid'],
#         'resultcode': '000',
#         'result': result,
#     }
#     return result


def predict_caller(diagram, predict_func):
    """
    调用预测模型
    :param diagram:
    :param predict_func:
    :return:
    """
    try:
        diagram = json.loads(diagram.decode())
    except (json.decoder.JSONDecodeError, TypeError):
        print('illegal json')
        raise IbaRequestError

    encrypt = True if (isinstance(diagram['encrypt'], bool) and diagram['encrypt']) or \
                      (isinstance(diagram['encrypt'], str) and diagram['encrypt'].upper() == 'TRUE') else False

    plaint_text = decrypt_sentences(diagram['text'], encrypt)
    try:
        predict_result = predict_func(plaint_text)
    except Exception as e:
        print('call predict failed')
        predict_result = None
        # raise IbaPredictError

    return predict_result, diagram


def predict_pre(diagram, predict_func):
    """
    flask调用预测
    :param diagram:
    :param predict_func:
    :return:
    """
    try:
        predict_result, req_dict = predict_caller(diagram, predict_func)
    except IbaRequestError as e:
        print('predict_pre error', e)
        predict_result = None
        req_dict = None

    return {
        'messageid': req_dict['messageid'] if predict_result else None,
        'clientid': req_dict['clientid'] if predict_result else None,
        'resultcode': '000' if predict_result else '001' if req_dict else '011',
        'result': predict_result
    }


def predict_pre_dict_args(diagram, predict_func, key):
    """
    flask调用预测，带key
    :param diagram:
    :param predict_func:
    :param tagname:
    :return:
    """
    try:
        predict_result, req_dict = predict_caller(diagram, predict_func)
    except IbaRequestError as e:
        print('predict_pre_dict_args error', e)
        predict_result = None
        req_dict = None

    predict_result_list = list()

    if predict_result:
        for m in predict_result:
            predict_result_list.append(m.get(key))

    return {
        'messageid': req_dict['messageid'] if req_dict else None,
        'clientid': req_dict['clientid'] if req_dict else None,
        'resultcode': '000' if predict_result else '001' if req_dict else '011',
        'result': predict_result_list if predict_result else predict_result
    }


# 下面这2个是临时的
def predict_caller_func_args_ext(diagram, predict_func, arg):
    """
    调用预测模型
    :param diagram:
    :param predict_func:
    :return:
    """
    try:
        diagram = json.loads(diagram.decode())
    except (json.decoder.JSONDecodeError, TypeError):
        print('illegal json')
        raise IbaRequestError

    encrypt = True if (isinstance(diagram['encrypt'], bool) and diagram['encrypt']) or \
                      (isinstance(diagram['encrypt'], str) and diagram['encrypt'].upper() == 'TRUE') else False

    plaint_text = decrypt_sentences(diagram['text'], encrypt)
    try:
        predict_result = predict_func(arg, plaint_text)
    except Exception as e:
        print('call predict failed')
        predict_result = None
        # raise IbaPredictError

    return predict_result, diagram


def predict_pre_func_args_ext(diagram, predict_func, key):
    """
    flask调用预测，带key
    :param diagram:
    :param predict_func:
    :param tagname:
    :return:
    """
    try:
        predict_result, req_dict = predict_caller_func_args_ext(diagram, predict_func, key)
    except IbaRequestError as e:
        print('predict_pre_func_args_ext error', e)
        predict_result = None
        req_dict = None

    return {
        'messageid': req_dict['messageid'] if predict_result else None,
        'clientid': req_dict['clientid'] if predict_result else None,
        'resultcode': '000' if predict_result else '001' if req_dict else '011',
        'result': predict_result
    }


def decrypt_sentences(sentences, encrypt=False):
    """
    text解密
    :param sentences:
    :param encrypt:
    :return:
    """
    if encrypt:
        pc = prpcrypt(get_config().get('encryptKey', 'key'))
        if isinstance(sentences, list):
            return [pc.decrypt(bytes(item, encoding='utf-8')) for item in sentences]
        elif isinstance(sentences, str):
            return pc.decrypt(bytes(sentences, encoding='utf-8'))
        return None
    else:
        return sentences

