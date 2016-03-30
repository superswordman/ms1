import os
import csv
class test1():
    def upload_avator(self):
        return os.system("C:\\Users\\leo\\Desktop\\upload_avator.exe")
        
    def checkcsv(self,filepath,x,y,text):
        csvreader = csv.reader(file(filepath))
        csvlist = []
        
        for row in csvreader:
            csvlist.append(row)

        if csvlist[x][y] == text:
            print 'good'
            return True
        else:
            print 'oh no'
            return Fasle

        #ttt



test = test1()
test.checkcsv("d:/test/xls/history.csv",1,0,'iphone6change1')
test.checkcsv("d:/test/xls/history.csv",1,0,'iphone6change')
test.checkcsv("d:/test/xls/history.csv",1,1,'3')
test.checkcsv("d:/test/xls/history.csv",1,9,'[app]')
