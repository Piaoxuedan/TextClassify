#coding=utf-8
import os
import sys
import re 
import jieba

class Feature:
    def __init__(self,input_path):
        self.input_path = input_path
        self.allClass = []
        self.termDic = dict()
        self.termClassDic = dict()
        self.termClassList = dict()
        self.ClassWord_tuple=[]
        for (dirname,dirs,files) in os.walk(self.input_path):  #第一个为起始路径；第二个为起始路径下的文件夹；起始路径下的文件
            for eachdir in dirs:
                self.allClass.append(eachdir)
                
    def buildItemSets(self):
        with open('stop.txt','r') as s:
            stopword_list = s.readlines()
        for i in xrange(0,len(stopword_list)):
            word = stopword_list[i].strip()
            stopword_list[i] = word
        for eachclass in self.allClass:
            #print eachclass
            eachClassWordSet = set()
            #ClassWord_tuple= []
            eachClassWordList = []
            current_path = os.path.join(self.input_path,eachclass) #把目录和文件名合成一个路径
            #print current_path
            for (dirname,dirs,filenames) in os.walk(current_path):
                for filename in filenames:
                    #tup=(str(dirname),str(filename))
                    dirname_2 = re.sub(r'data/ClassFile\\','',dirname)
                    self.ClassWord_tuple.append(dirname_2)
                    self.ClassWord_tuple.append(filename)
                    with open(os.path.join(current_path,filename),'r') as f:
                        eachFileSet = set()
                        eachfile_list = []
                        #eachfile_tuple = ()
                        content = f.read()
                        content = self.process_line(content)
                        words = jieba.cut(content.strip(), cut_all=False) #精确模式
                        for word in words:
                            word = word.strip()
                            if word.encode('utf8') not in stopword_list and len(word)>2:
                                eachfile_list.append(word)
                                eachFileSet.add(word)
                                eachClassWordSet.add(word)
                    eachClassWordList.append(eachFileSet)
                    self.ClassWord_tuple.append(eachfile_list)
            self.termDic[eachclass] = eachClassWordSet 
            self.termClassDic[eachclass] = eachClassWordList



    def writeFileToCut(self):
        final_tuple=self.ClassWord_tuple
        for i in range(0,len(final_tuple),3):
            dirpath='D:/Project/classifier python/final_case/SogouCCut/' + final_tuple[i] + '/' +final_tuple[i+1]
            dirpath_2 = re.sub(r'.txt','.cut',dirpath)
            #print dirpath
            eachfile_words = final_tuple[i+2]
            word_file = open(dirpath_2,'w')
            for word in eachfile_words:
                word_file.write(word.encode('utf-8') + " ")




    def process_line(self, content):
        try:
            #content = re.sub('[\dnbsp]','',content)
            content = re.sub('[\&nbsp]','',content)
            return content
        except UnicodeDecodeError:            
            return content
            
   
    def ChiCalc(self,a, b, c, d):
        result = float(pow((a*d - b*c), 2)) /float((a+c) * (a+b) * (b+d) * (c+d))
        return result
                                
    
    def featureSelection(self,K):
        termCountDic = dict()
        for key in self.termDic:
            print "%s计算卡方值开始"%key
            classWordSets = self.termDic[key]
            classTermCountDic = dict()
            for eachword in classWordSets: 
                a = 0
                b = 0
                c = 0
                d = 0
                for eachclass in self.termClassDic:
                    if eachclass == key: 
                        for eachdocset in self.termClassDic[eachclass]:
                            if eachword in eachdocset:
                                a = a + 1
                            else:
                                c = c + 1
                    else:
                        for eachdocset in self.termClassDic[eachclass]:
                            if eachword in eachdocset:
                                b = b + 1
                            else:
                                d = d + 1
                eachwordcount = self.ChiCalc(a, b, c, d)
                classTermCountDic[eachword] = eachwordcount
            sortedClassTermCountDic = sorted(classTermCountDic.items(), key=lambda d:d[1], reverse=True)
            count = 0
            subDic = dict()
            for i in range(K):
                subDic[sortedClassTermCountDic[i][0]] = sortedClassTermCountDic[i][1]
            termCountDic[key] = subDic
        return termCountDic
     
     
    def writeFeatureToFile(self,termCountDic, fileName):
        featureSet = set()
        for key in termCountDic:
            for eachkey in termCountDic[key]:
                featureSet.add(eachkey)
        file = open(fileName, 'w')
        print "开始写入特征词"
        #for feature in featureSet:
            #print feature
        for feature in featureSet:
            #stripfeature = feature.strip(" ")
            if len(feature) > 0 and feature != " " :
                file.write(feature.encode('utf8')+"\n")
                #print(feature)
        file.close()           
               
                
if __name__ == "__main__":
    featureTest = Feature('data/ClassFile')
    featureTest.buildItemSets()
    #print "分词，构建词典集合结束"
    featureTest.writeFileToCut()
    termCountDic = featureTest.featureSelection(200)
    featureTest.writeFeatureToFile(termCountDic, 'feature.txt')
    
    
        
    
        
