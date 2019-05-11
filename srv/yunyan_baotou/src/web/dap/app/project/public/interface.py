# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_restful import Api, Resource
from . import bp_public
from ..tools import predict_pre, predict_pre_dict_args, predict_pre_func_args_ext
from dmp.gongan.gz_case_money.moneyCount import sum_money as predict_amount
from dmp.gongan.gz_wp_ner.predict import ner_predict as predict_items
from dmp.gongan.storm_crim_classify.extcode import digital_info_extract as predict_ext
from dmp.gongan.Entity_name.predict import ner_predict as predict_name
from dmp.gongan.gz_case_date.predict import ner_predict as predict_date


api = Api()
api.init_app(bp_public)


class PubDateResource(Resource):
    """
    时间ner
    """
    def post(self):
        resp = predict_pre_dict_args(request.data, predict_date, 'date')
        return jsonify(resp)


class PubNameResource(Resource):
    """
    用户名ner
    """
    def post(self):
        resp = predict_pre_dict_args(request.data, predict_name, 'per')
        return jsonify(resp)


class PubPhoneNumbResource(Resource):
    """
    电话号ner
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'phoneNum')
        return jsonify(resp)


class PubIdcardResource(Resource):
    """
    身份证ner
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'identifier')
        return jsonify(resp)


class PubWeixinResource(Resource):
    """
    微信号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'wx')
        return jsonify(resp)


class PubWeiboResource(Resource):
    """
    微博号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'weibo')
        return jsonify(resp)


class PubQQResource(Resource):
    """
    QQ号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'qq')
        return jsonify(resp)


class PubPlateNumResource(Resource):
    """
    车牌号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'carinfo')
        return jsonify(resp)


class PubCreditcardResource(Resource):
    """
    信用卡号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'creditCard')
        return jsonify(resp)


class PubMomoResource(Resource):
    """
    默默号
    """
    def post(self):
        resp = predict_pre_func_args_ext(request.data, predict_ext.extract_digital_spec, 'momo')
        return jsonify(resp)


class PubItemsResource(Resource):
    """
    涉案物品
    """
    def post(self):
        resp = predict_pre(request.data, predict_items)
        return jsonify(resp)


class PubAmountResource(Resource):
    """
    涉案金额
    """
    def post(self):
        resp = predict_pre(request.data, predict_amount)
        return jsonify(resp)


# add
api.add_resource(PubDateResource, '/predict/110/date')
api.add_resource(PubNameResource, '/predict/110/username')
api.add_resource(PubPhoneNumbResource, '/predict/110/phoneNum')
api.add_resource(PubIdcardResource, '/predict/110/identifier')
api.add_resource(PubWeiboResource, '/predict/110/weibo')
api.add_resource(PubWeixinResource, '/predict/110/weixin')
api.add_resource(PubQQResource, '/predict/110/qq')
api.add_resource(PubPlateNumResource, '/predict/110/carinfo')
api.add_resource(PubCreditcardResource, '/predict/110/creditCard')
api.add_resource(PubMomoResource, '/predict/110/momo')
api.add_resource(PubItemsResource, '/predict/110/items')
api.add_resource(PubAmountResource, '/predict/110/msum')



