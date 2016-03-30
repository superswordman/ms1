#coding=utf-8 
import linecache
import os
import chardet
import sys
import MySQLdb
default_encoding = 'utf-8'
filepath = 'C:\Users\kai\Desktop\mysql\gua.txt'
savefilepath = 'C:\Users\kai\Desktop\mysql\gua1.txt'
linecount = len(open(filepath,'rU').readlines())
baihua = '【白话】'
xiang = '《象》曰'
gua_dict = {0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:'','numlist':''}

startline = 1
def initGua():
    gua_dict = {0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:'','numlist':''}

def bGuaYaoYong(inputstr,compstr):
    nPos = inputstr.find(compstr)
    if nPos >= 0 :
        return True
    return False



#def createGugsql():



guatext = ''

while(startline < linecount):    
    tstr = linecache.getline(filepath,startline) 
    startline += 1
    if bGuaYaoYong(tstr,baihua):
        continue
    elif bGuaYaoYong(tstr,xiang):
        continue    
    else:
        guatext += tstr
       
saveHandle = open(savefilepath,'w')
saveHandle.write(guatext)  
saveHandle.close()
print guatext.decode('utf8')    
