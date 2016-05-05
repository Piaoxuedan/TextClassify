#coding: utf-8
import os 
import sys
import re
import jieba
import math

class feature:
	def __init__(self,input_path):
		self.input_path = input_path
		self.allClass = []
		self.ClassWord_tuple = []
		self.FileWord_tuple = []
		self.total_count =0
		#self.idf_dic = dict()
		#self.idf_tuple=[]
		for (dirname,dirs,files) in os.walk(self.input_path):
			for eachdir in dirs:
				self.allClass.append(eachdir)

	def buildItemSets(self):
		with open('stop.txt','r') as s:
			stopword_list = s.readlines()
		for i in xrange(0,len(stopword_list)):
			word = stopword_list[i].strip()
			stopword_list[i] = word
		for eachclass in self.allClass:
			current_path = os.path.join(self.input_path,eachclass)
			for (dirname,dirs,filenames) in os.walk(current_path):
				feature_tf_dic = dict()
				for filename in filenames:
					self.total_count = self.total_count + 1
					classname = re.sub(r'data/ClassFile\\','',dirname)
					if classname not in self.ClassWord_tuple:
						self.ClassWord_tuple.append(classname)
					self.FileWord_tuple.append(classname)
					self.FileWord_tuple.append(filename)
					with open(os.path.join(current_path,filename),'r') as f:
						vector_tf_dic = {}
						content = f.read()
						content = self.process_line(content)
						words = jieba.cut(content.strip(),cut_all=False)
						for word in words:
							word = word.strip()
							if word.encode('utf-8') not in stopword_list and len(word)>1:
								vector_tf_dic[word] = vector_tf_dic.get(word,0) + 1
								feature_tf_dic[word] = feature_tf_dic.get(word,0) + 1
					self.FileWord_tuple.append(vector_tf_dic)
				self.ClassWord_tuple.append(feature_tf_dic)
		#print self.ClassWord_tuple	
		#print self.FileWord_tuple

	def process_line(self,content):
		try:
			content = re.sub(r'[\&nbsp]','',content)
			content = re.sub(r'[0-9]','',content)
			return content
		except UnicodeDecodeError:
			return content

	def feature_IDF(self):
		len_of_classword = len(self.ClassWord_tuple)
		len_of_fileword = len(self.FileWord_tuple)
		idf_dic = dict()
		for i in xrange(0,len_of_classword,2):			
			#self.idf_tuple.append(self.ClassWord_tuple[i])
			class_dic = self.ClassWord_tuple[i+1]		
			for key in class_dic.keys():
				doc_count = 0				
				for j in xrange(0,len_of_fileword,3):
					if key in self.FileWord_tuple[j+2]:
						doc_count += 1
				idf_dic[key] = doc_count
			#self.idf_tuple.append(idf_dic)
		return idf_dic

	def tfidf_cal(self,idf_dic):
		len_of_classword = len(self.ClassWord_tuple)
		tfidf_tuple = []		
		for i in xrange(0,len_of_classword,2):
			tfidf_tuple.append(self.ClassWord_tuple[i])
			zidian = self.ClassWord_tuple[i+1]
			tfidf_dic = dict()
			for key in zidian.keys():
				tf = zidian[key]
				df = idf_dic[key]
				idf = math.log(float(self.total_count/df))
				tf_idf = float(tf) * float(idf)
				tfidf_dic[key] = tf_idf
			tfidf_tuple.append(tfidf_dic)
		return tfidf_tuple

	def feature_select(self,tfidf_tuple,k,filename):
		len_of_tfidf = len(tfidf_tuple)
		tfidf_sorted = []
		for i in xrange(0,len_of_tfidf,2):
			tfidf_sorted_dic = dict()
			classname = tfidf_tuple[i]
			#print tfidf_tuple[i+1]
			tfidf_sorted.append(classname)
			tfidf_sorted_dic = sorted(tfidf_tuple[i+1].items(),key = lambda d:d[1],reverse = True)
			tfidf_sorted.append(tfidf_sorted_dic)
		len_of_tfidf_sorted = len(tfidf_sorted)
		feature =[]
		file = open(filename,'w+') 
		for j in xrange(0,len_of_tfidf_sorted,2):
			belonged_class = tfidf_sorted[j]
			sorted_list = tfidf_sorted[j+1][0:k]
			for w in xrange(len(sorted_list)):
				feature.append(sorted_list[w][0])
				file.write(sorted_list[w][0].encode('utf-8'))
				file.write('\n')
		file.close()

if __name__ == '__main__':
	featureTest = feature('data/ClassFile')
	featureTest.buildItemSets()
	dic = featureTest.feature_IDF()
	tfidf = featureTest.tfidf_cal(dic)
	featureTest.feature_select(tfidf,20,'feature.txt')

