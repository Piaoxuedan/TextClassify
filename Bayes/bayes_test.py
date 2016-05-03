#coding:utf-8
import pickle
import jieba
import nltk
import os
import re

class Test:
    def __init__(self,input_path):
        self.input_path = input_path
        self.folder = []
        for (dirname,dirs,files) in os.walk(self.input_path):
            for eachdir in dirs:
                self.folder.append(os.path.join(dirname,eachdir))

    def document_features(self,document):
        document_words = set(document) #文件中所有词的集合
        features = {}
        (classifier,word_features)= Test.read_cache(self)
        for word in word_features:
            features['contains(%s)'%word] = (word in document_words)
        return features

    def read_cache(self):
        with open('.cache_file','rb') as cache_file:
            classifier = pickle.load(cache_file)
            word_features = pickle.load(cache_file)
            cache_file.close()
        return classifier,word_features

    def classify(self):
        classify_result = {}
        (classifier,word_features)= Test.read_cache(self)
        for folder in self.folder:
            correct = 0
            error = 0
            for file in os.listdir(folder):
                total = 0
                txt = open(folder + os.sep + file,'r')
                try:
                    text = txt.read()
                except UnicodeDecodeError:
                    pass
                txt.close()
                word_cut = jieba.cut(text, cut_all = False)
                word_list = list(word_cut)
                user_test_data = Test.document_features(self,word_list)
                classified = classifier.classify(user_test_data)
                classify_result[file] = classified
                cur_class = re.sub(r'.\\TestFile\\','',folder)
                if classified != cur_class:
                    error += 1
                else:
                    correct +=1
                print (cur_class,file,'is classifed to', classified)
            rate = float(correct)/ float(error + correct)
            print rate

if __name__ == '__main__':
    bayes_test = Test(".\\TestFile")
    bayes_test.classify()