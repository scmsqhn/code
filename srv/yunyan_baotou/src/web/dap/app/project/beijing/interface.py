# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_restful import Api, Resource
from . import bp_beijing
from ..tools import predict_pre
from dmp.gongan.storm_crim_classify.gonganpred import criminalpredict as predict_classify
from dmp.gongan.bj_crim_farmer_classify.gonganpred import criminalpredict as predict_farmer
from dmp.gongan.bj_110_address.predict import ner_predict as predict_addr_ner
from dmp.gongan.bj_crim_suspect_classify.gonganpred import criminalpredict as predict_suspect
from dmp.gongan.bj_crim_loc_classify.gonganpred import criminalpredict as predict_region
from dmp.gongan.guangxi_crim_vehicle_classify.gonganpred import criminalpredict as predict_vehicle
from dmp.gongan.bj_crim_ner_suspect_character.predict_ner import predict_ner_height, predict_ner_stature, \
    predict_ner_nation, predict_ner_sex, predict_ner_age, \
    predict_ner_accent, predict_ner_character, predict_ner_hairstyle


api = Api()
api.init_app(bp_beijing)


def predict_case_classify(sentences):
    predict_result = predict_classify(sentences)

    out_result = list()
    for i in range(len(predict_result)):
        if predict_result[i] == '涉农':
            predict_str_farmer = [sentences[i]]
            pred_farmer = predict_farmer(predict_str_farmer)
            out_result.extend(pred_farmer)
        else:
            out_result.append(predict_result[i])
    return out_result


class BJClassifyResource(Resource):
    """
    案情分类
    """
    def post(self):
        resp = predict_pre(request.data, predict_case_classify)
        return jsonify(resp)


class BJAddressResource(Resource):
    """
    地址ner
    """
    def post(self):
        resp = predict_pre(request.data, predict_addr_ner)
        return jsonify(resp)


class BJHeightResource(Resource):
    """
    身高
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_height)
        return jsonify(resp)


class BJStatureResource(Resource):
    """
    体型
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_stature)
        return jsonify(resp)


class BJNationResource(Resource):
    """
    民族 
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_nation)
        return jsonify(resp)


class BJSexResource(Resource):
    """
    性别 
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_sex)
        return jsonify(resp)


class BJAgeResource(Resource):
    """
    年龄 
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_age)
        return jsonify(resp)


class BJAccentResource(Resource):
    """
    口音 
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_accent)
        return jsonify(resp)


class BJCharacterResource(Resource):
    """
    特殊特征 
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_character)
        return jsonify(resp)


class BJHairstyleResource(Resource):
    """
    发型
    """
    def post(self):
        resp = predict_pre(request.data, predict_ner_hairstyle)
        return jsonify(resp)


class BJSuspectClassifyResource(Resource):
    """
    嫌疑人数量分类
    """
    def post(self):
        resp = predict_pre(request.data, predict_suspect)
        return jsonify(resp)


class BJVehicleClassifyResource(Resource):
    """
    作案交通工具分类
    """
    def post(self):
        resp = predict_pre(request.data, predict_vehicle)
        return jsonify(resp)


class BJRegionClassifyResource(Resource):
    """
    作案部位分类
    """
    def post(self):
        resp = predict_pre(request.data, predict_region)
        return jsonify(resp)


api.add_resource(BJClassifyResource, '/predict/110/caseClassify')
api.add_resource(BJAddressResource, '/predict/110/loc')
api.add_resource(BJHeightResource, '/predict/110/height')
api.add_resource(BJStatureResource, '/predict/110/stature')
api.add_resource(BJNationResource, '/predict/110/nation')
api.add_resource(BJSexResource, '/predict/110/sex')
api.add_resource(BJAgeResource, '/predict/110/age')
api.add_resource(BJAccentResource, '/predict/110/accent')
api.add_resource(BJCharacterResource, '/predict/110/character')
api.add_resource(BJHairstyleResource, '/predict/110/hairstyle')
api.add_resource(BJSuspectClassifyResource, '/predict/110/suspectClassify')
api.add_resource(BJVehicleClassifyResource, '/predict/110/vehicleClassify')
api.add_resource(BJRegionClassifyResource, '/predict/110/region')



