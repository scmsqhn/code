import os
import sys
import re

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append('/data')

dist_baotou = ['青山区', '昆都仑区', '东河区', '九原区', '石拐区', '白云鄂博矿区',
               '固阳县', '土默特右旗', '达尔罕茂明安联合旗']


def bert_result_to_dicts(infile1):
    dict_res = dict()
    dict_res['SHEQU'] = {}
    dict_res['CJWH'] = {}
    dict_res['ZRCZ'] = {}
    dict_res['JLX'] = {}
    dict_res['XIAOQU'] = {}
    dict_res['ZUTUAN'] = {}
    dict_res['JZW'] = {}
    f11 = open(infile1, 'r', encoding='utf-8')
    lines = []
    for line in f11.readlines():
        if line[-3] == 'r':
            continue
            pass
        lines.append(line)
    f11.close()

    for line in lines:
        line = re.sub("\n", "", line)
        while line:
            index1 = line.find('/')
            index2 = line.find(' ')
            word = line[0:index1]
            pos = line[index1 + 1:index2]
            line = line[index2 + 1:]
            if len(word) > 1 and pos in dict_res.keys():
                if word not in dict_res[pos].keys():
                    dict_res[pos][word] = 1
                else:
                    dict_res[pos][word] += 1

    return dict_res


def dict_extend(dict_p, min_num, out_file):
    my_dict = []
    for key in dict_p.keys():
        for w in dict_p[key].keys():
            if dict_p[key][w] < min_num:
                continue
                pass
            my_dict.append((w, str(dict_p[key][w]), key))

    for word in dist_baotou:
        my_dict.append((word, '9999', 'DIST'))

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # 栋号
    for le in letters:
        my_dict.append((le + '栋', '9999', 'DONGHAO'))
        for i in range(1, 10):
            my_dict.append((le + str(i) + '栋', '9999', 'DONGHAO'))

    tmp_sym = ['付', '附', '新', '老', '甲', '乙', '丙', '东', '西', '南', '北', '中']
    for i in range(2000):
        my_dict.append((str(i) + '栋', '9999', 'DONGHAO'))
        if i < 1000:
            my_dict.append(('0' + str(i) + '栋', '9999', 'DONGHAO'))
        for ts in tmp_sym:
            my_dict.append((ts + str(i) + '栋', '9999', 'DONGHAO'))
            if i < 1000:
                my_dict.append((ts + '0' + str(i) + '栋', '9999', 'DONGHAO'))
        if 0 < i < 10:
            my_dict.append(('00' + str(i) + '栋', '9999', 'DONGHAO'))
            for ts in tmp_sym:
                my_dict.append((ts + '00' + str(i) + '栋', '9999', 'DONGHAO'))

    # 户室号
    for i in range(4000):
        my_dict.append((str(i) + '室', '9999', 'HSH'))
        my_dict.append((str(i) + '户', '9999', 'HSH'))
        if 0 < i < 10:
            my_dict.append(('0' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('00' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('附' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('付' + str(i) + '室', '9999', 'HSH'))
        if 9 < i < 100:
            my_dict.append(('0' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('00' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('附' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('付' + str(i) + '室', '9999', 'HSH'))
        if 99 < i < 1000:
            my_dict.append(('0' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('附' + str(i) + '室', '9999', 'HSH'))
            my_dict.append(('付' + str(i) + '室', '9999', 'HSH'))

    # 单元号
    for i in range(100):
        my_dict.append((str(i) + '单元', '9999', 'DYH'))
        my_dict.append((str(i) + '排', '9999', 'DYH'))
        for ts in tmp_sym:
            my_dict.append((ts + str(i) + '单元', '9999', 'DYH'))
            my_dict.append((ts + str(i) + '排', '9999', 'DYH'))

    # 楼层
    for i in range(200):
        my_dict.append((str(i) + '层', '9999', 'LOUC'))

    # 门牌号
    for i in range(1200):
        my_dict.append((str(i) + '号', '9999', 'MPH'))
        my_dict.append((str(i) + '号甲', '9999', 'MPH'))
        my_dict.append((str(i) + '号乙', '9999', 'MPH'))
        for ts in tmp_sym:
            my_dict.append((ts + str(i) + '号', '99999', 'MPH'))
        if 0 < i < 10:
            my_dict.append(('0' + str(i) + '号', '9999', 'MPH'))
            my_dict.append(('00' + str(i) + '号', '9999', 'MPH'))
            my_dict.append(('0' + str(i) + '号甲', '9999', 'MPH'))
            my_dict.append(('00' + str(i) + '号乙', '9999', 'MPH'))
            for ts in tmp_sym:
                my_dict.append((ts + '0' + str(i) + '号', '99999', 'MPH'))
                my_dict.append((ts + '00' + str(i) + '号', '99999', 'MPH'))
        if 9 < i < 100:
            my_dict.append(('0' + str(i) + '号', '9999', 'MPH'))
            my_dict.append(('0' + str(i) + '号甲', '9999', 'MPH'))
            my_dict.append(('0' + str(i) + '号乙', '9999', 'MPH'))
            for ts in tmp_sym:
                my_dict.append((ts + '0' + str(i) + '号', '99999', 'MPH'))

    # 村居委会
    for i in range(1, 20):
        if (str(i) + '街委', '9999', 'CJWH') not in my_dict:
            my_dict.append((str(i) + '街委', '9999', 'CJWH'))

    # 自然村组
    for i in range(1, 20):
        if (str(i) + '组', '9999', 'ZRCZ') not in my_dict:
            my_dict.append((str(i) + '组', '9999', 'ZRCZ'))
        if (str(i) + '队', '9999', 'ZRCZ') not in my_dict:
            my_dict.append((str(i) + '队', '9999', 'ZRCZ'))
        if (str(i) + '区', '9999', 'ZRCZ') not in my_dict:
            my_dict.append((str(i) + '区', '9999', 'ZRCZ'))

    f1 = open(out_file, 'w', encoding='utf-8')
    for wp in my_dict:
        f1.write(wp[0])
        f1.write(' ')
        f1.write(wp[1])
        f1.write(' ')
        f1.write(wp[2])
        f1.write('\n')
    f1.close()


if __name__ == '__main__':

    bert_result_file = basedir+'/bt_trans_12_1_100000_pos.txt'  # bert模型切分结果
    dict_z = bert_result_to_dicts(bert_result_file)  # bert模型切分结果统计出的词典
    dict_file = basedir + '/dict_extend.txt'  # 最终的词典文件
    dict_extend(dict_z, 10, dict_file)  # 扩充词典, 得到最终的词典

