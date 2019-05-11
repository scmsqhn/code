import pickle
import os
import re
basedir = os.path.dirname(os.path.abspath(__file__))


def save_var(var,fl):
    f = open(fl,'wb')
    pickle.dump(var,f)    
    print('var save ok')


def read_var(fl):
    image_lists=pickle.load(open(fl,'rb'))
    return image_lists


def clr(line):
    line = re.sub("\n","",line)
    line = re.sub("\r","",line)
    line = re.sub(" ","",line)
    return line


def strQ2B(ustring):
    ustring = str(ustring)
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12200:
            inside_code = 32
        elif 65374 >= inside_code >= 65281:
            inside_code -= 65248
        rstring+=chr(inside_code)
    return rstring


def find_sym(line1, regular):
    pattern1 = re.compile(regular)
    res1 = pattern1.findall(line1)
    return res1


def pre_trans(line):
    res = {}
    symbol = {}
    index1 = line.find('包头市')
    index2 = line.find('包头')
    if index1 >= 0:
        line = line[index1 + 3:]
    elif index2 >= 0:
        line = line[index2 + 2:]

    line = strQ2B(line)
    line = line.strip()
    #line = re.sub("[^\u4e00-\u9fa5a-zA-Z0-9-]", "-", line)

    r0 = find_sym(line, "(号$)")
    if r0:
        line = re.sub("(号)", "室", line)
        symbol["室"] = r0[0]

    r0 = find_sym(line, "(号楼|幢)")
    if r0:
        line = re.sub("(号楼|幢)", "栋", line)
        symbol["栋"] = r0[0]

    r0 = find_sym(line, "([0-9a-zA-Z])座(\d+)楼")
    if r0:
        line = re.sub("([0-9a-zA-Z])座(\d+)楼", "\\1栋\\2层", line)
        key = [r0[0][1]+'层', r0[0][0]+'栋']
        value = [r0[0][1]+'楼', r0[0][0]+'座']
        for i in range(len(key)):
            symbol[key[i]] = value[i]

    r0 = find_sym(line, "([a-zA-Z0-9])座")
    if r0:
        line = re.sub("([a-zA-Z0-9])座", "\\1栋", line)
        key = r0[0]+'栋'
        value = r0[0]+'座'
        symbol[key] = value

    r0 = find_sym(line, "[0-9]{6,20}")
    if r0:
        line = re.sub("[0-9]{6,20}", r0[0][0:3], line)
        symbol[r0[0][0:3]] = r0[0]

    r0 = find_sym(line, "(\d+)号院")
    if r0:
        line = re.sub("(\d+)号院", "\\1号", line)
        symbol[r0[0] + '号'] = r0[0] + '号院'

    r0 = find_sym(line, "(\d+)栋(\d+)号(\d+)号$")
    if r0:
        line = re.sub("(\d+)栋(\d+)号(\d+)号$", "\\1栋\\2单元\\3室", line)
        symbol[r0[0][2]+'室'] = r0[0][2]+'号'
        symbol[r0[0][1] + '单元'] = r0[0][1] + '号'

    r0 = find_sym(line, "(\d+)栋(\d+)号(\d+)室$")
    if r0:
        line = re.sub("(\d+)栋(\d+)号(\d+)室$", "\\1栋\\2单元\\3室", line)
        symbol[r0[0][1] + '单元'] = r0[0][1] + '号'

    r0 = find_sym(line, "(\d+)栋(\d+)号$")
    if r0:
        line = re.sub("(\d+)栋(\d+)号$", "\\1栋\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)号(\d+)号$")
    if r0:
        line = re.sub("(\d+)号(\d+)号$", "\\1号\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)号付(\d+)号$")
    if r0:
        line = re.sub("(\d+)号付(\d+)号$", "\\1号付\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)栋(\d+)排(\d+)号")
    if r0:
        line = re.sub("(\d+)栋(\d+)排(\d+)号", "\\1栋\\2单元\\3室", line)
        symbol[r0[0][2] + '室'] = r0[0][2] + '号'
        symbol[r0[0][1] + '单元'] = r0[0][1] + '排'

    r0 = find_sym(line, "(\d+)排(\d+)栋(\d+)号")
    if r0:
        line = re.sub("(\d+)排(\d+)栋(\d+)号", "\\1单元\\2栋\\3室", line)
        symbol[r0[0][2] + '室'] = r0[0][2] + '号'
        symbol[r0[0][0] + '单元'] = r0[0][0] + '排'

    r0 = find_sym(line, "(\d+)栋(\d+)号$")
    if r0:
        line = re.sub("(\d+)栋(\d+)号$", "\\1栋\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)栋付(\d+)号$")
    if r0:
        line = re.sub("(\d+)栋付(\d+)号$", "\\1栋付\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)栋(\d+)楼(\d+)号$")
    if r0:
        line = re.sub("(\d+)栋(\d+)楼(\d+)号$", "\\1栋\\2层\\3室", line)
        symbol[r0[0][2]+'室'] = r0[0][2]+'号'
        symbol[r0[0][1] + '层'] = r0[0][1] + '楼'

    r0 = find_sym(line, "(\d+)楼付(\d+)号$")
    if r0:
        line = re.sub("(\d+)楼付(\d+)号$", "\\1栋付\\2室", line)
        symbol[r0[0][1]+'室'] = r0[0][1]+'号'
        symbol[r0[0][0] + '栋'] = r0[0][0] + '楼'

    r0 = find_sym(line, "(\d+)单元(\d+)楼(\d+)号")
    if r0:
        line = re.sub("(\d+)单元(\d+)楼(\d+)号", "\\1单元\\2层\\3室", line)
        key = [r0[0][2] + '室', r0[0][1] + '层']
        value = [r0[0][2] + '号', r0[0][1] + '楼']
        for i in range(len(key)):
            symbol[key[i]] = value[i]

    r0 = find_sym(line, "(\d+)楼(\d+)号$")
    if r0:
        line = re.sub("(\d+)楼(\d+)号$", "\\1栋\\2室", line)
        symbol[r0[0][1] + '室'] = r0[0][1] + '号'
        symbol[r0[0][0] + '栋'] = r0[0][0] + '楼'

    r0 = find_sym(line, "(\d+)单元(\d+)号")
    if r0:
        line = re.sub("(\d+)单元(\d+)号", "\\1单元\\2室", line)
        key = r0[0][1] + '室'
        symbol[key] = r0[0][1] + '号'

    r0 = find_sym(line, "(\d+)排(\d+)号(\d+)户")
    if r0:
        line = re.sub("(\d+)排(\d+)号(\d+)户", "\\1单元\\2栋\\3室", line)
        symbol[r0[0][2] + '室'] = r0[0][2] + '户'
        symbol[r0[0][1] + '栋'] = r0[0][1] + '号'
        symbol[r0[0][0] + '单元'] = r0[0][0] + '排'

    r0 = find_sym(line, "(\d+)排(\d+)号$")
    if r0:
        line = re.sub("(\d+)排(\d+)号$", "\\1单元\\2室", line)
        symbol[r0[0][1] + '室'] = r0[0][1] + '号'
        symbol[r0[0][0] + '单元'] = r0[0][0] + '排'

    r0 = find_sym(line, "(\d+)层(\d+)号$")
    if r0:
        line = re.sub("(\d+)层(\d+)号$", "\\1层\\2室", line)
        key = r0[0][1]+'室'
        value = r0[0][1]+'号'
        symbol[key] = value

    r0 = find_sym(line, "(\d+)楼(\d+)单元(\d+)层(\d+)号")
    if r0:
        line = re.sub("(\d+)楼(\d+)单元(\d+)层(\d+)号", "\\1栋\\2单元\\3层\\4室", line)
        symbol[r0[0][3] + '室'] = r0[0][3] + '号'
        symbol[r0[0][0] + '栋'] = r0[0][0] + '楼'

    r0 = find_sym(line, "(\d+)楼(\d+)单元")
    if r0:
        line = re.sub("(\d+)楼(\d+)单元", "\\1栋\\2单元", line)
        symbol[r0[0][0] + '栋'] = r0[0][0] + '楼'

    r0 = find_sym(line, '一(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("一(栋|单元|层|室|号街坊)", "1\\1", line)
        key = '1'+r0[0]
        symbol[key] = '一'+r0[0]

    r0 = find_sym(line, '二(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("二(栋|单元|层|室|号街坊)", "2\\1", line)
        key = '2'+r0[0]
        symbol[key] = '二'+r0[0]

    r0 = find_sym(line, '三(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("三(栋|单元|层|室|号街坊)", "3\\1", line)
        key = '3'+r0[0]
        symbol[key] = '三'+r0[0]

    r0 = find_sym(line, '四(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("四(栋|单元|层|室|号街坊)", "4\\1", line)
        key = '4'+r0[0]
        symbol[key] = '四'+r0[0]

    r0 = find_sym(line, '五(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("五(栋|单元|层|室|号街坊)", "5\\1", line)
        key = '5'+r0[0]
        symbol[key] = '五'+r0[0]

    r0 = find_sym(line, '六(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("六(栋|单元|层|室|号街坊)", "6\\1", line)
        key = '6'+r0[0]
        symbol[key] = '六'+r0[0]

    r0 = find_sym(line, '七(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("七(栋|单元|层|室|号街坊)", "7\\1", line)
        key = '7'+r0[0]
        symbol[key] = '七'+r0[0]

    r0 = find_sym(line, '八(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("八(栋|单元|层|室|号街坊)", "8\\1", line)
        key = '8'+r0[0]
        symbol[key] = '八'+r0[0]

    r0 = find_sym(line, '九(栋|单元|层|室|号街坊)')
    if r0:
        line = re.sub("九(栋|单元|层|室|号街坊)", "9\\1", line)
        key = '9'+r0[0]
        symbol[key] = '九'+r0[0]

    r0 = find_sym(line, '零(栋|单元|层|室)')
    if r0:
        line = re.sub("零(栋|单元|层|室)", "0\\1", line)
        key = '0'+r0[0]
        symbol[key] = '零'+r0[0]

    line = re.sub("\(.+?\)", "", line)
    line = re.sub("（.+?）", "", line)
    line = re.sub("（.+?）", "", line)

    res[line] = symbol

    return res


def split_final(symbols, sp_dict):
    sentence = list(symbols.keys())[0]
    dict1 = symbols[sentence]
    sentence_ = list(sp_dict.keys())[0]
    dict2 = sp_dict[sentence_]
    for k1 in dict1:
        for k2 in dict2:
            if k1 in dict2[k2]:
                dict2[k2] = dict2[k2].replace(k1, dict1[k1])
                break
                pass
    sp_dict[sentence_] = dict2
    return sp_dict


'''
def function(original_sentence):
    # original_sentence为原始地址
    trans_sentence = pre_trans(original_sentence)  # 规则转化地址, 以及对应的转化信息
    sentence = list(trans_sentence.keys())[0]  # 将要进行切分的地址
    split_result = function1(sentence)  # 切分
    # split_result格式：{original_sentence: {'区':, '单元号':, '小区名':,...}}
    split_final_result = split_final(trans_sentence, split_result)  # 还原切分结果
    return split_final_result
'''


if __name__ == "__main__":

    '''
    book = xlrd.open_workbook(basedir + "\\data\\11111.xls")
    sheets = book.sheet_names()
    address_cla = ['区', '单元号', '小区名', '市', '建筑物', '户室号', '村居委会', '栋号',
                   '楼号', '楼层', '省', '社区', '组团名称', '自然村组', '街路巷名', '门牌号']
    data_test = []
    for index, sh in enumerate(sheets):
        sheet = book.sheet_by_index(index)
        rows, cols = sheet.nrows, sheet.ncols
        for row in range(5, 105):
            tmp1 = {}
            tmp2 = {}
            key = sheet.cell(row, 2).value
            for i in range(16):
                cell = sheet.cell(row, i+3)
                value = cell.value
                tmp2[address_cla[i]] = value
            tmp1[key] = tmp2
            data_test.append(tmp1)
        break

    for data in data_test:
        key = list(data.keys())[0]
        trans_sentence = pre_trans(key)  # 规则转化地址, 以及对应的转化信息
        # sentence = list(trans_sentence.keys())[0]  # 将要进行切分的地址
        split_final_result = split_final(trans_sentence, data)  # 还原切分结果
        print(split_final_result)
    '''

    '''
    original_sentence = '贵阳市观山湖区金华镇林东路三区5-5-5-5室'  # 原始地址
    trans_sentence = pre_trans(original_sentence)  # 规则转化地址, 以及对应的转化信息
    sentence = list(trans_sentence.keys())[0]  # 将要进行切分的地址
    split_result = function1(sentence)  # 切分输出结果
    split_final_result = split_final(trans_sentence, split_result)  # 还原切分结果
    '''

    '''
    ss = '云岩区威清路4号贵阳市检察院建和兴苑小区2单元18-02室'
    rr = pre_trans(ss)
    tt = list(rr.keys())[0]
    dict_1 = {tt:{'门牌号':'5号','楼号':'5栋','单元号':'5单元','户室号':'5室'}}
    zz = split_final(rr, dict_1)

    line4 = '5-5室'
    line4 = re.sub("(\d+)-(\d+室)$", "\\1层\\2", line4)
    line4 = re.sub("(\d+)-(\d+室)$", "\\1层\\2", line4)
    line4 = re.sub("(\d+)-(\d+)-(\d+)-(\d+)$", "\\1号\\2栋\\3单元\\4室", line4)
    line4 = re.sub("([a-zA-Z0-9])座", "\\1栋", line4)
    '''
