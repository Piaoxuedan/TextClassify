#coding: utf-8
import os
import sys
import re
import jieba
import math

class Test_vectorize:
	def __init__(self,input_path):
		self.input_path = input_path
		self.allClass = []
		self.FileWord_tuple = []
		for (dirname,dirs,files) in os.walk(self.input_path):
			for eachdir in dirs:
				self.allClass.append(eachdir)

	def read_feadture(self,feature_txt):
		feature_file = open(feature_txt,'r')
		feature_content = feature_file.read().split('\n')
		feature_file.close()
		feature = list()
		for each_feature in feature_content:
			each_feature = each_feature.split(" ")
			if (len(each_feature)==1):
				feature.append(each_feature[0])
		self.feature = []
		for k in range(0,len(feature)-1):
			self.feature.append(feature[k])
		
	def buildItemSets(self):
		with open('stop.txt','r') as s:
			stopword_list = s.readlines()
		for i in xrange(0,len(stopword_list)):
			word = stopword_list[i].strip()
			stopword_list[i] = word
		for eachclass in self.allClass:
			current_path = os.path.join(self.input_path,eachclass)
			for (dirname,dirs,filenames) in os.walk(current_path):
				for filename in filenames:
					classname = re.sub(r'data/TestFile\\','',dirname)
					self.FileWord_tuple.append(classname)
					self.FileWord_tuple.append(filename)
					vector_tf_list = []
					with open(os.path.join(current_path,filename),'r') as f:
						content = f.read()
						content = self.process_line(content)
						words = jieba.cut(content.strip(),cut_all = False)
						cut_words = []
						for word in words:
							word = word.strip()
							if word.encode('utf-8') not in stopword_list and len(word)>1:
								cut_words.append(word)
					for feature in self.feature:
						tf = 0
						#print feature
						for left_word in cut_words:
							#print left_word.encode('utf-8')
							if left_word.encode('utf-8') == feature:
								#print Ture
								tf +=1
							else:
								#print False
								tf = tf
						value = feature + ":" + str(tf)
						vector_tf_list.append(value)
					self.FileWord_tuple.append(vector_tf_list)

	def process_line(self,content):
		try:
			content = re.sub(r'[\&nbsp]','',content)
			content = re.sub(r'[0-9]','',content)
			return content
		except UnicodeDecodeError:
			return content

	def write_to_file(self,filename):
	 	file = open(filename,'w+')
	 	len_of_fileword = len(self.FileWord_tuple)
	 	for i in xrange(0,len_of_fileword,3):
	 		file.write(self.FileWord_tuple[i])
	 		file.write(" ")
	 		last_vector = self.FileWord_tuple[i+2]
	 		for content in last_vector:
	 			file.write(content)
	 			file.write(" ")
	 		file.write('\n')

if __name__ == '__main__':
	text_vector = Test_vectorize('data/TestFile')
	text_vector.read_feadture('feature.txt')
	text_vector.buildItemSets()
	text_vector.write_to_file('test.txt')


