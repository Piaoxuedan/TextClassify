#coding:utf-8
import os
import sys
import re
import jieba
import math

class FilesCut:
	def __init__(self,input_path):
		self.input_path = input_path
		self.all_class = []
		self.class_word_tuple = []
		#self.class_dic_set = dict()
		#self.class_dic_list = dict()
		for (dirname,dirs,files) in os.walk(self.input_path):
			for eachdir in dirs:
				self.all_class.append(eachdir)

	def build_item_sets(self):
		with open('stop.txt','r') as f:
			stopword_list = f.readlines()
		for i in xrange(0,len(stopword_list)):
			word = stopword_list[i].strip()
			stopword_list[i] = word
		class_dic_set = dict()
		class_dic_list = dict()
		for eachclass in self.all_class:
			eachclass_word_set = set()
			eachclass_word_list = []
			current_path = os.path.join(self.input_path,eachclass)
			for (dirname,dirs,filenames) in os.walk(current_path):
				for filename in filenames:
					dirname_2 = re.sub(r'data/TestFile\\','',dirname)
					self.class_word_tuple.append(dirname_2)
					self.class_word_tuple.append(filename)
					with open(os.path.join(current_path,filename),'r') as f2:
						eachfile_set = set()
						eachfile_list = []
						content = f2.read()
						content = self.process_line(content)
						words = jieba.cut(content.strip(),cut_all = False)
						for word in words:
							word = word.strip()
							if word.encode('utf8') not in stopword_list and len(word) > 2:
								eachfile_list.append(word)
								eachfile_set.add(word)
								eachclass_word_set.add(word)
						eachclass_word_list.append(eachfile_set)
					self.class_word_tuple.append(eachfile_list)
			class_dic_set[eachclass] = eachclass_word_set
			class_dic_list[eachclass] = eachclass_word_list
		return class_dic_set,class_dic_list

	def process_line(self, content):
		try:
			content = re.sub('[\&nbsp]','',content)
			return content
		except UnicodeDecodeError:            
			return content

	def writefileTocut(self,dirpath):
		final_tuple = self.class_word_tuple
		for i in range(0,len(final_tuple),3):
			dirpath_2 = dirpath + final_tuple[i] 
			dirpath_3 = self.path(dirpath_2)
			dirpath_4 = dirpath_3 + '/' + final_tuple[i+1]
			eachfile_words = final_tuple[i+2]
			word_file = open(dirpath_4,'w')
			for word in eachfile_words:
				word_file.write(word.encode('utf-8') + " ")

	def path(self,checkpath):
		isExits = os.path.exists(checkpath)
		if not isExits:
			os.makedirs(checkpath)
		else:
			pass
		return checkpath 

class feature_selection:
	def __init__(self,class_dic_1,class_dic_2):
		#super(feature_selection,self).__init__('data/TestFile')
		self.class_dic_set = class_dic_1
		self.class_dic_list = class_dic_2
		
	def ChiCalc(self,a, b, c, d):
		result = float(pow((a*d - b*c), 2)) /float((a+c) * (a+b) * (b+d) * (c+d))
		return result

	def featureSelection(self,K):
		termCountDic = dict()
		for key in self.class_dic_set:
			#print "%s计算卡方值开始"%key
			classWordSets = self.class_dic_set[key]
			classTermCountDic = dict()
			for eachword in classWordSets: 
				a = 0
				b = 0
				c = 0
				d = 0
				for eachclass in self.class_dic_list:
					if eachclass == key: 
						for eachdocset in self.class_dic_list[eachclass]:
							if eachword in eachdocset:
								a = a + 1
							else:
								c = c + 1
					else:
						for eachdocset in self.class_dic_list[eachclass]:
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
		file.close()   

class cal_tfidf:
	def __init__(self,input_path):
		self.input_path = input_path
		self.all_class = []
		for (dirname,dirs,files) in os.walk(self.input_path):
			for eachdir in dirs:
				self.all_class.append(eachdir)

	def read_feature(self,feature_txt):
		feature_file = open(feature_txt,'r')
		feature_content = feature_file.read().split('\n')
		feature_file.close()
		feature = list()
		for each_feature in feature_content:
			each_feature = each_feature.split(" ")
			if (len(each_feature)==1):
				feature.append(each_feature[0])
		feature_2 = []
		for k in range(0,len(feature)-1):
			feature_2.append(feature[k])
		print len(feature_2)
		return feature_2

	#对测试集进行特征向量表示
	def readFileToList(self):
		dic = dict()
		for eachclass in self.all_class:
			#print eachclass
			currentClass_path = self.input_path + '/' + eachclass + '/'
			writeFilePathPrefix = os.path.dirname(os.path.abspath('__file__')).strip("") + "\TestCut\\" + eachclass + '\\' 
			eachclasslist = list()
			for (dirname,dirs,files) in os.walk(currentClass_path):
				for eachfile in files:
					eachfile_path = writeFilePathPrefix + eachfile
					#eachfile_path = re.sub(r'\\','/',eachfile_path)
					eachfile_c = open(eachfile_path,'r')
					eachfile_content = eachfile_c.read()
					eachfilewords = eachfile_content.split(" ")
					eachclasslist.append(eachfilewords)
					#print len(eachclasslist)
			dic[eachclass] = eachclasslist
		return dic

	#计算特征的逆文档频率
	def feature_IDF(self,dic,feature,df_filename):
		df_file = open(df_filename,"w")
		df_file.close()
		df_file = open(df_filename,"a")
		total_doc_count = 0
		idf_feature = dict()
		df_feature = dict()
		for eachfeature in feature:
			doc_feature = 0
			for key in dic:
				total_doc_count = total_doc_count + len(dic[key])
				class_files = dic[key]
				#print class_files
				#print 'woqu'
				for eachfile in class_files:
					if eachfeature in eachfile:
						doc_feature = doc_feature + 1
			#计算特征的逆文档频率
			feature_value = math.log(float(total_doc_count)/(doc_feature + 1))
			df_feature[eachfeature] = doc_feature
			#写入文件，特征的文档频率
			df_file.write(eachfeature + " " + str(doc_feature) + "\n")
			idf_feature[eachfeature] = feature_value
		df_file.close()
		return idf_feature

	#计算feature's tf-idf 值
	def tfidf_Cal(self,feature,dic,idf_feature,filename):
		file = open(filename,'w')
		file.close()
		file = open(filename,'a')
		for key in dic:
			classfiles = dic[key]
			classid = self.all_class.index(key)
			#print classid
			for eachfile in classfiles:
				#print type(eachfile)  //list
				#对每个文件进行特征向量转化
				#file.write(str(classid) + " ")
				file.write(str(key) + " ")
				for i in range(len(feature)):
					if  feature[i] in eachfile:
						current_feature = feature[i]
						feature_count = eachfile.count(feature[i])
						tf = float(feature_count)/(len(eachfile))
						# 计算逆文档频率
						feature_value = idf_feature[current_feature] * tf
					else:
						feature_value = 0
						#file.write(str(i+1)+":"+str(feature_value)+" ")
					file.write(feature[i]+":"+str(feature_value)+" ")
				file.write("\n")

if __name__ == "__main__":
	test_cut = FilesCut('data/TestFile')
	(class_dic_1,class_dic_2) = test_cut.build_item_sets()
	test_cut.writefileTocut('D:/Project/classifier python/final_case/TestCut/')
	#test_feature = feature_selection(class_dic_1,class_dic_2)
	#termCountDic = test_feature.featureSelection(50)
	#test_feature.writeFeatureToFile(termCountDic, 'test_feature.txt')
	feature_weight = cal_tfidf('D:/Project/classifier python/final_case/TestCut')
	dic = feature_weight.readFileToList()
	feature = feature_weight.read_feature("feature.txt")
	#print(len(feature))
	idf_feature_2 = feature_weight.feature_IDF(dic,feature,"test_df_feature.txt")
	feature_weight.tfidf_Cal(feature,dic,idf_feature_2,"test.txt")

    

