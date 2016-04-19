#coding: utf-8
import os
import sys
import re
import math
from numpy import *

class importTrain:
    def __init__(self,input_path,feature_file):
        self.input_path = input_path
        self.feature_file = feature_file
        featurepath = os.path.join(self.input_path, self.feature_file)
        f1 = open(featurepath ,'r')
        featureContent = f1.read().split('\n')
        self.feature = list()
        for eachfeature in featureContent:
            eachfeature = eachfeature.split(" ")
            if(len(eachfeature) == 1):
                self.feature.append(eachfeature[0])
        self.columncount = len(self.feature)
        print self.columncount

    def importData(self,filename):
        datapath = self.input_path + filename
        f = open(datapath,'r')
        vectors = f.readlines()
        rowcount = len(vectors)
        returnMat = zeros((rowcount,self.columncount))
        class_label_vector = []
        index = 0
        for vector in vectors:
            vector = vector.strip()
            each_vector_list = vector.split(' ')
            class_label_vector.append(each_vector_list[0])
            processing_data = []
            for i in xrange(1,len(each_vector_list)):
                each_data = re.search(r':(.+?)',each_vector_list[i])
                #each_data = re.sub(r"[\u4e00-\u9fa5]","",each_data)
                each_data = each_data.group()
                each_data = re.sub(r":","",each_data)
                #print each_data
                processing_data.append(each_data)
            #print len(processing_data)
            returnMat[index, : ] = processing_data[0:]
            index += 1
        if returnMat is not zeros:
            print True
        else:
            print False
        return returnMat,class_label_vector

    def Normalized(self,dataSet):
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        ranges = maxVals - minVals
        dataSet_norm = zeros(shape(dataSet))
        row = dataSet.shape[0]
        dataSet_norm = dataSet - tile(minVals,(row,1))
        dataSet_norm = dataSet_norm/tile(ranges,(row,1))
        return dataSet_norm ,ranges,minVals

    def classify(self,train_file,test_file):
        (trainMat, trainClass) = self.importData('train.txt')
        (testMat,testClass) = self.importData('test.txt')
        rowSize = trainMat.shape[0]
        vectorid = 0
        for vector in testMat:
            vectorid += 1
            expand_vector = tile(vector,(rowSize,1))
            diffMat = expand_vector - trainMat
            #print diffMat
            sq_diffMat = diffMat ** 2
            #print sq_diffMat
            #print 'sdkfjsflks'
            sq_distances = sq_diffMat.sum(axis = 1,dtype = float)
            distances = sq_distances ** 0.5
            minValue = distances.min(0)
            index = 0
            for minvector in distances:                
                if minvector == minValue:
                    index = index
                else:
                    index +=1 
            judged_id = trainClass[index]
            #print judged_id
            given_id = testClass[vectorid-1]
            #print given_id
            #print 'haha'
     
if __name__ == "__main__":
    inputdata = importTrain('D:/Project/classifier python/final_case/','test_feature.txt')
    inputdata.classify("train.txt","test.txt")
    