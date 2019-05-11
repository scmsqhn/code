from flask import Flask
# from ..config import config


def create_app(config_name):
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False

    ################################
    # 注册项目接口
    ########
    # 公共
    ########
    # > 时间
    # > 用户名
    # 电话号
    # 身份证
    # 微信号
    # 微博号
    # QQ号
    # 车牌号
    # 信用卡号
    # 默默号
    # 涉案物品
    # 涉案金额
    from .project.public import bp_public
    app.register_blueprint(bp_public, url_prefix='/public')

    ########
    # 贵州
    ########
    # 作案手段
    # 作案方式
    # 作案部位
    # 身份证
    # 电话串号
    # 电话号（联系人）
    # 电话卡号
    # 车牌号
    # Mac地址
    # 车架号
    # 引擎号
    # 案发地址
    # * 涉案物品
    # * 涉案金额
    from .project.guizhou import bp_guizhou
    app.register_blueprint(bp_guizhou, url_prefix='/guizhou')

    ########
    # 山东
    ########
    # 案情分类
    # 案发地址
    from .project.shandong import bp_shandong
    app.register_blueprint(bp_shandong, url_prefix='/shandong')

    ########
    # 北京
    ########
    # 案情分类
    # 案发地址
    from .project.beijing import bp_beijing
    app.register_blueprint(bp_beijing, url_prefix='/beijing')

    ########
    # 广西
    ########
    # 案情分类
    # 案发地址
    # from .project.guangxi import bp_guangxi
    # app.register_blueprint(bp_guangxi, url_prefix='/guangxi')

    return app


