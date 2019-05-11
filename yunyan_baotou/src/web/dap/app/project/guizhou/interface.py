# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_restful import Api, Resource
from . import bp_guizhou
from ..tools import predict_pre
from dmp.gongan.gz_case_detail.caseDetails import user_idcard, phone_sn, phone_number, phone_card,\
    plate_number, mac_addr, vehicle_sn, engine_sn, case_location
from dmp.gongan.gz_crim_loc_classify.gonganpred import criminalpredict as predict_loc # 部位
from dmp.gongan.gz_crim_method_classify.gonganpred import criminalpredict as predict_method # 方式
from dmp.gongan.gz_crim_type_classify.gonganpred import criminalpredict as predict_type # 手段
from dmp.gongan.gz_case_money.moneyCount import sum_money as predict_amount
from dmp.gongan.gz_wp_ner.predict import ner_predict as predict_items


api = Api()
api.init_app(bp_guizhou)


class GZMethodClassifyResource(Resource):
    """
    作案手段
    """
    def post(self):
        resp = predict_pre(request.data, predict_method)
        return jsonify(resp)


class GZTypeClassifyResource(Resource):
    """
    作案方式
    """
    def post(self):
        resp = predict_pre(request.data, predict_type)
        return jsonify(resp)


class GZLocClassifyResource(Resource):
    """
    作案部位
    """
    def post(self):
        resp = predict_pre(request.data, predict_loc)
        return jsonify(resp)


class GZIdcardResource(Resource):
    """
    身份证
    """
    def post(self):
        resp = predict_pre(request.data, user_idcard)
        return jsonify(resp)


class GZPhoneSnResource(Resource):
    """
    电话串号
    """
    def post(self):
        resp = predict_pre(request.data, phone_sn)
        return jsonify(resp)


class GZPhoneNumResource(Resource):
    """
    电话号（联系人）
    """
    def post(self):
        resp = predict_pre(request.data, phone_number)
        return jsonify(resp)


class GZPhoneSimcardResource(Resource):
    """
    电话卡号
    """
    def post(self):
        resp = predict_pre(request.data, phone_card)
        return jsonify(resp)


class GZPlateNumbResource(Resource):
    """
    车牌号
    """
    def post(self):
        resp = predict_pre(request.data, plate_number)
        return jsonify(resp)


class GZMacAddrResource(Resource):
    """
    Mac地址
    """
    def post(self):
        resp = predict_pre(request.data, mac_addr)
        return jsonify(resp)


class GZVehicleSnResource(Resource):
    """
    车架号
    """
    def post(self):
        resp = predict_pre(request.data, vehicle_sn)
        return jsonify(resp)


class GZEngineSnResource(Resource):
    """
    引擎号
    """
    def post(self):
        resp = predict_pre(request.data, engine_sn)
        return jsonify(resp)


class GZCaseAddrResource(Resource):
    """
    案发地址
    """
    def post(self):
        resp = predict_pre(request.data, case_location)
        return jsonify(resp)


class GZItemsResource(Resource):
    """
    涉案物品
    """
    def post(self):
        resp = predict_pre(request.data, predict_items)
        return jsonify(resp)


class GZAmountResource(Resource):
    """
    涉案金额
    """
    def post(self):
        resp = predict_pre(request.data, predict_amount)
        return jsonify(resp)


api.add_resource(GZMethodClassifyResource, '/method/predict')
api.add_resource(GZTypeClassifyResource, '/type/predict')
api.add_resource(GZLocClassifyResource, '/loc/predict')
api.add_resource(GZIdcardResource, '/method/idcard')
api.add_resource(GZPhoneSnResource, '/method/phonesn')
api.add_resource(GZPhoneNumResource, '/method/phonenumber')
api.add_resource(GZPhoneSimcardResource, '/method/simcard')
api.add_resource(GZPlateNumbResource, '/method/platenum')
api.add_resource(GZMacAddrResource, '/method/macaddr')
api.add_resource(GZVehicleSnResource, '/method/vehiclesn')
api.add_resource(GZEngineSnResource, '/method/enginesn')
api.add_resource(GZCaseAddrResource, '/method/caselocation')
api.add_resource(GZItemsResource, '/method/algor/ner')
api.add_resource(GZAmountResource, '/method/gzcase/msum')


