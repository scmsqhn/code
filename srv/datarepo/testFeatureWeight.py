import math
import sys
ClassCode =  [ '财经','房产','股票','家居','科技','时政','娱乐' ]
textCutBasePath = "SogouDataCut/"
testDocumentCount = 200
documentCount = 1200
trainDocumentCount = 8400

# 读取特征
def readFeature(featureName):
    featureFile = open(featureName, 'r')
    featureContent = featureFile.read().split('\n')
    featureFile.close()
    feature = list()
    for eachfeature in featureContent:
        eachfeature = eachfeature.split(" ")
        if (len(eachfeature)==2):
            feature.append(eachfeature[1])
    return feature

# 读取特征的文档计数
def readDfFeature(dffilename):
    dffeaturedic = dict()
    dffile = open(dffilename, "r")
    dffilecontent = dffile.read().split("\n")
    dffile.close()
    for eachline in dffilecontent:
        eachline = eachline.split(" ")
        if len(eachline) == 2:
            dffeaturedic[eachline[0]] = eachline[1]
            # print(eachline[0] + ":"+eachline[1])
    # print(len(dffeaturedic))
    return dffeaturedic

# 对测试集进行特征向量表示
def readFileToList(textCutBasePath, ClassCode, documentCount, testDocumentCount):
    dic = dict()
    for eachclass in ClassCode:
        currClassPath = textCutBasePath + eachclass + "/"
        eachclasslist = list()
        
        for i in range(documentCount, documentCount+testDocumentCount):
            #print(currClassPath+str(i)+".cut")
            eachfile = open(currClassPath+str(i)+".txt")
            eachfilecontent = eachfile.read()
            eachfilewords = eachfilecontent.split(" ")
            eachclasslist.append(eachfilewords)
            # print(eachfilewords)
        dic[eachclass] = eachclasslist
    return dic

def TFIDFCal(feature, dic,dffeaturedic,filename):
    file = open(filename, 'w')
    file.close()
    file = open(filename, 'a')
    # classid = 0
    for key in dic:
        # print(key)
        classFiles = dic[key]
        classid = ClassCode.index(key)
        for eachfile in classFiles:
            # 对每个文件进行特征向量转化
            file.write(str(classid)+" ")
            for i in range(len(feature)):
                if feature[i] in eachfile:
                    currentfeature = feature[i]
                    featurecount = eachfile.count(feature[i])
                    tf = float(featurecount)/(len(eachfile))
                    # 计算逆文档频率
                    idffeature = math.log(float(trainDocumentCount+1)/(int(dffeaturedic[currentfeature])+2))
                    featurevalue = idffeature * tf
                    file.write(str(i+1)+":"+str(featurevalue) + " ")
            file.write("\n")

if __name__ == '__main__':
    # 对200至250序号的文档作为测试集
    feature = readFeature("SVMFeature.txt")
    dffeaturedic = readDfFeature("dffeature.txt")
    dic = readFileToList(textCutBasePath, ClassCode, documentCount, testDocumentCount)
    TFIDFCal(feature, dic, dffeaturedic, "test.svm")
