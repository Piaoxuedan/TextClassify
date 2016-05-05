#coding: utf-8
import os 
import sys
import re
import jieba

class feature:
	def __init__(self,input_path):
		self.input_path = input_path
		self.allClass = []
		self.ClassWord_tuple = []
		self.FileWord_tuple = []
		#self.feature_tf_dic = dict()
		#self.vector_tf_dic = dict() 
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
					classname = re.sub(r'data/ClassFile\\','',dirname)
					if classname not in self.ClassWord_tuple:
						self.ClassWord_tuple.append(classname)
						self.FileWord_tuple.append(classname)
					self.FileWord_tuple.append(filename)
					with open(os.path.join(current_path,filename),'r') as f:
						#eachfile_list = []
						vector_tf_dic = {}
						content = f.read()
						content = self.process_line(content)
						words = jieba.cut(content.strip(),cut_all=False)
						for word in words:
							word = word.strip()
							if word.encode('utf-8') not in stopword_list and len(word)>1:
								vector_tf_dic[word] = vector_tf_dic.get(word,0) + 1
								feature_tf_dic[word] = feature_tf_dic.get(word,0) + 1
								#eachfile_list.append(word)
					self.FileWord_tuple.append(vector_tf_dic)
				self.ClassWord_tuple.append(feature_tf_dic)
		print self.ClassWord_tuple 	
		print self.FileWord_tuple

	def process_line(self,content):
		try:
			content = re.sub(r'[\&nbsp]','',content)
			content = re.sub(r'[^0-9]','',content)
			return content
		except UnicodeDecodeError:
			return content

	#def feature_IDF(self,)
if __name__ == '__main__':
	featureTest = feature('data/ClassFile')
	featureTest.buildItemSets()

