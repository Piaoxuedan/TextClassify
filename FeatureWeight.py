# coding:utf-8
import Feature
import math
import sys
import os
import jieba
import re

class FeatureWeight:
	def __init__(self,input_path):
		self.input_path = input_path
		self.all_class = []
		for (dirname,dirs,files) in os.walk(self.input_path):
			for eachdir in dirs:
				self.all_class.append(eachdir)

	def readFeature(self,featureName):
		#featurePath = "D:\\Project\\classifier python\\final_case\\"+ featureName 
		featureFile = open(featureName,'r')
		featureContent = featureFile.read().split('\n')
		featureFile.close()
		feature = list()
		for eachfeature in featureContent:
			eachfeature = eachfeature.split(" ")
			if (len(eachfeature)==1):
				feature.append(eachfeature[0])
		#print feature
		return feature

	#读取所有类别的训练样本到字典中，每个文档是一个list
	def readFileToList(self):
		dic = dict()
		for eachclass in self.all_class:
			#print eachclass
			currentClass_path = self.input_path + '/' + eachclass + '/'
			writeFilePathPrefix = os.path.dirname(os.path.abspath('__file__')).strip("") + "\SogouCCut\\" + eachclass + '\\' 
			eachclasslist = list()
			for (dirname,dirs,files) in os.walk(currentClass_path):
				for eachfile in files:
					eachfile_path = writeFilePathPrefix + eachfile
					#print eachfile_path
					#eachfile_path = re.sub(r'\\','/',eachfile_path)
					#print eachfile_path
					eachfile_c = open(eachfile_path,'r')
					eachfile_content = eachfile_c.read()
					#print eachfile_content
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
			print eachfeature
			doc_feature = 0
			for key in dic:
				total_doc_count = total_doc_count + len(dic[key])
				class_files = dic[key]
				for eachfile in class_files:
					if eachfeature in eachfile:
						#print type(eachfeature)
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
			print key
			#print dic[key]
			#print len(dic[key])
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
	FeatureWeight = FeatureWeight('D:/Project/classifier python/final_case/SogouCCut')
	dic = FeatureWeight.readFileToList()
	feature = FeatureWeight.readFeature("feature.txt")
	print(len(feature))
	idf_feature = FeatureWeight.feature_IDF(dic,feature,"df_feature.txt")
	FeatureWeight.tfidf_Cal(feature,dic,idf_feature,"train.txt")
