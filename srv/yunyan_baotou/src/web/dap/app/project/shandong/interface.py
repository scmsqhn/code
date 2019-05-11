# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from . import bp_shandong
from ..tools import predict_pre
from dmp.gongan.shandong_crim_classify.gonganpred import criminalpredict as predict_classify
from dmp.gongan.sd_110_address.predict import ner_predict as predict_ner_addr

api = Api()
api.init_app(bp_shandong)


class SDClassifyResource(Resource):
    """
    案情分类
    """
    def post(self):
        resp = predict_pre(request.data, predict_classify)
        return jsonify(resp)


class SDAddressResource(Resource):
    """
    地址ner
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_addr)
        return jsonify(resp)


# add
api.add_resource(SDClassifyResource, '/predict/110/caseClassify')
api.add_resource(SDAddressResource, '/predict/110/loc')


