#!/usr/bin/python
#coding:utf8
'''
Abstract Factory of webservice generate
'''


import sys
sys.path.append('../..')
import myconfig
import random
from flask import Flask, Response
import myconfig
from flask import Flask
import addr_service_interface
from addr_service_interface import *

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(main,url_prefix='/normalization')

if __name__=='__main__':
    #app.run(host='0.0.0.0', debug=True, port=7944, use_reloader=True, threaded=False)
    app.run(host='0.0.0.0', debug=True, port=5901 , use_reloader=True, threaded=True)
