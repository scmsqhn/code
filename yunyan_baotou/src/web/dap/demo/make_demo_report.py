# coding=utf-8
from dmp.store.db import default_sql as Db
from dmp.model.cbc_report import generate_cbc_report

if __name__ == "__main__":
    # 增加虚拟列
    # alter table r_user_eval_report add score float generated always as (report_score->'$."指标评估"."s"');
    # 生成企业评价相关算子
    # update_sqlstr = "UPDATE r_indexs_method " \
    #                 "SET method = concat(" \
    #                 "'sql://SELECT count(*) FROM b_enterprise_public_sentiment s '," \
    #                 "' INNER JOIN b_enterprise_info i ON s.enterprise_name = i.`name` '," \
    #                 "' WHERE label_type LIKE \\'%', name, '%\\''," \
    #                 "' AND pub_date > %(start_time)s '," \
    #                 "' AND pub_date < %(end_time)s '," \
    #                 "' AND i.id = %(user_id)s')" \
    #                 "where parent_id = 'b98ecd82972911e6a79c0242ac110002'"
    # Db.execute(update_sqlstr)
    result = Db.query('select id from b_enterprise_info')
    model_ids = Db.query('select modelid from b_app_model')
    change_time = "update r_user_eval_report set report_time = %(report_time)s, " \
                "report_score = JSON_SET(report_score, '$.\"报告信息\".\"报告时间\"', " \
                "%(report_time)s) " \
                "where report_time > '2016-10-20'"
    for row in result:
        user_id = row[0]
        for model_id in model_ids:
            for i in range(1, 11):
                generate_cbc_report({'user_id': user_id, 'model_id': model_id[0], 'start_time': '2016/{0}/01'.format(i),
                                     'end_time': '2016/{0}/01'.format(i + 1)})
                Db.execute(change_time, {'report_time': '2016/{0}/05'.format(i+1)})
