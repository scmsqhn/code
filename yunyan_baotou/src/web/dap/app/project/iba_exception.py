# -*- coding: utf-8 -*-


class IbaRequestError(Exception):
    def __init__(self, err='请求异常'):
        Exception.__init__(self, err)


class IbaPredictError(Exception):
    def __init__(self, err='预测接口异常'):
        Exception.__init__(self, err)

