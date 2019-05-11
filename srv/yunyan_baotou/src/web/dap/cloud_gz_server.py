# coding=utf-8
import flask
from dmp.model.cloud_gz_report import *
from dutil.log import logger

app = flask.Flask(__name__)


# 云中贵州测试接口
@app.route('/cloud_gz', methods=['POST'])
def cloud_guizhou_report():
    log.debug(flask.request.data)
    param = json.loads(flask.request.data)
    logger.debug(json.dumps(param, indent=2, ensure_ascii=False))
    return generate_cloudgz_report(param['user_id'], param['model_id'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7778, use_reloader=True, threaded=True)
