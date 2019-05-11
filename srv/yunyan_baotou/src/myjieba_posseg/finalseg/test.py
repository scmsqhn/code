import jieba
import re
import pdb
import os
CURPATH = os.path.dirname(os.path.realpath(__file__))
DEBUG = False

level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组",\
        "门牌号","小区名","组团名称","楼号","栋号",\
        "单元号","楼层","户室号","sent","rw"]

def get_ready_my_dict():
    with open(os.path.join(CURPATH,"standard_addr.json")) as f:
        cont = f.read()
        standard_addr = json.loads(cont)
    standard_dct = {}
    ks = []
    vs = []
    for item in standard_addr['RECORDS']:
        v = item['name']
        k = item['type']
        ks.append(k)
        vs.append(v)
    keys = list(set(ks))
    values = list(set(vs))

    for k in keys:
        standard_dct[k] = []

    for item in standard_addr['RECORDS']:
        v = item['name']
        k = item['type']
        if not v in standard_dct[k]:
            standard_dct[k].append(v)
    standard_dct['xiaoqu']=[]
    standard_dct['juweihui']=[]
    standard_dct['shequ']=[]
    for key in standard_dct:
        print(key,standard_dct[key][:3])
    return standard_dct


#'doornum', 'county', 'province', 'street', 'community', 'ld', 'room', 'unit', 'group', 'committee', 'village', 'city', 'floor'
# 门牌号　ｘｘｘ　省　街路巷　ｘｘｘ　楼栋　房号　单元　组团　乡村　村　市  楼层
for key in standard_dct:
    print(key,standard_dct[key][:3])

with open(os.path.join(CURPATH,'xq2.txt'),'r') as g:
    lines = g.readlines()

level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组",\
        "门牌号","小区名","组团名称","楼号","栋号",\
        "单元号","楼层","户室号","sent","rw"]

#pattern = re.compile(r'^(.{2,5}省)?(.{2,5}市)?(.{2,5}县|.{2,5}(?<!小)区(?!路))?([\u4e00-\u9fa5]+?(?:乡|镇(?!委会)|办事处|社区服务中心|社区|片区))?([\u4e00-\u9fa5]+(?:委会|村委会|村委会|村委员会|居委会|创业园|村(?![街道路巷民组苑])))?(?!委会)(?:服务中心)?(?<!商铺)(?:(?:[\u4e00-\u9fa5]+村(?![民街路巷道委]))?([\u4e00-\u9fa5]+(?:段|街|路|巷|道|地块|[东南西北]侧)(?!组)))?(?:空头户)?(.+?(?:村民组|居民组|组|寨|庄)(?![巷街道路组团]))?((?:散居|新|附|门面|门面房)?[a-zA-Z\d一二三四壹贰叁肆五六七八九十]+号(?:地块)?(?!楼)(?:附\d+号?!$)?|\d+$|散居\d+(?=\d0))?(?:交叉口)?(?!\d)([^一二三四壹贰叁肆五六七八九十散居附\d单元甲乙丙丁戊a-zA-Z]+(?:小区|园|苑|[首一二三四壹贰叁肆五六七八九十]期|花园|山美诗|方舟|城|居住区|新城|院|[\u4e00-\u9fa5])?(?<![一二三四壹贰叁肆五六七八九十甲乙丙丁戊])(?<!期))?([a-zA-Z\d\u4e00-\u9fa5]+(?:宿舍|大厦|广场|综合体|健身中心))?((?![一二三四壹贰叁肆五六七八九十壹]+栋)[^附]+(?:组团)(?:[a-zA-Z\d]+区)?|[东南西北壹贰叁伍拾\dA-Za-z一二三四壹贰叁肆五六七八九十]+区|甲乙丙丁戊)?((?:附)?[\da-zA-Z]+(?:号楼)|办公楼)?((?:经济适用房)?(?:商铺)?[\da-zA-Z首一二三四壹贰叁肆五六七八九十东南西北壹贰叁肆伍\-]+?[栋幢座](?:[\u4e00-\u9fa5]+阁)?)?([\da-zA-Z一二三四壹贰叁肆五六七八九十]+单元)?((?:[负附])?[\d一二三四壹贰叁肆五六七八九十a-zA-Z]+?[楼层]|[一二三四壹贰叁肆五六七八九十]+层)?((?:[\da-zA-Z]+型)?正?(?:[\da-zA-Z]+)*?[负附付夹底夹底地下层]*?[门面\da-zA-Z\-、]+[号幢室]+?(?:附[\d一二三四壹贰叁肆五六七八九十]+?号)?|\d+号|\d+|附?[\d一二三四壹贰叁肆五六七八九十]+号门面|[a-zA-Z]座|\d+0\d+)?(?:空挂户)?[\r\n]*?$')
#self.reg_pools_part_2.append([pattern,"省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","建筑物名称","组团名称","楼号","栋号","单元号","楼层","户室号"])

for k in keys:
    standard_dct[k] = []

for item in standard_addr['RECORDS']:
    v = item['name']
    k = item['type']
    if not v in standard_dct[k]:
        standard_dct[k].append(v)
standard_dct['xiaoqu']=[]
standard_dct['juweihui']=[]
standard_dct['shequ']=[]

#'doornum', 'county', 'province', 'street', 'community', 'ld', 'room', 'unit', 'group', 'committee', 'village', 'city', 'floor'
# 门牌号　ｘｘｘ　省　街路巷　ｘｘｘ　楼栋　房号　单元　组团　乡村　村　市  楼层
for key in standard_dct:
    print(key,standard_dct[key][:3])

with open(os.path.join(CURPATH,'xq2.txt'),'r') as g:
    lines = g.readlines()
    for line in lines:
        standard_dct['xiaoqu'].append(re.sub("[\r\n]","",line))
str_xiaoqu = "|".join(standard_dct['xiaoqu'])
str_xiaoqu = ("(?:%s)?"%str_xiaoqu)

with open(os.path.join(CURPATH,'jwh.txt'),'r') as g:
    lines = g.readlines()
    for line in lines:
        standard_dct['juweihui'].append(re.sub("[\r\n]","",line))

with open(os.path.join(CURPATH,'sq.txt'),'r') as g:
    lines = g.readlines()

with open("cut_result.txt","a+") as g:
    with open("add_total.txt","r") as f:
        lines = f.readlines()
        #删除括号内的文本
        txt = re.sub("(.+?)[\(（].+?[\)）]","\1",txt)
        #filter the useless charector
        txt = re.sub("[^\u4e00-\u9fa50-9a-zA-Z\-]","",txt)
        for line in lines:
            cuts = list(jieba.cut(line))
            g.write("%s\n"%(str(cuts)))

