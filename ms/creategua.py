#coding=utf-8 
import linecache
import chardet
import sys
import MySQLdb
default_encoding = 'utf-8'
filepath='C:\Users\kai\Desktop\mysql\gua1.txt'
linecount = len(open(filepath,'rU').readlines())
qiangua = ['初九，','九二，','九三，','九四，','九五，','上九，','用九','卦：']
kungua = ['初六，','六二，','六三，','六四，','六五，','上六，','用六','卦：']
yanggua = ['初九，','九二，','九三，','九四，','九五，','上九，','卦：']
yingua = ['初六，','六二，','六三，','六四，','六五，','上六，','卦：']
gua_dict = {0:'',1:'',2:'',3:'',4:'',5:'',6:'',7:'','name':'','gualist':''}

startline = 1
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='ms',port=3306,use_unicode=True, charset="utf8")
    cur=conn.cursor()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def initGua(dict):
    for k in dict:
        dict[k] = ''

def showGua(dict):
    for k in dict:
        print dict[k].decode('utf8')

def bGuaYaoYong(inputstr,compstr):
    nPos = inputstr.find(compstr)
    if nPos >= 0 :
        return True
    return False



def insertGua(dict):
    sqlStr = 'insert into gua values(\'' 
    sqlStr += dict['gualist'].decode('utf8') + '\',\'' + dict['name'].decode('utf8') + '\',\'' + dict[0].decode('utf8')
    sqlStr += '\',\'' + dict[1].decode('utf8') + '\',\'' +  dict[2].decode('utf8') + '\',\'' +  dict[3].decode('utf8') 
    sqlStr += '\',\'' + dict[4].decode('utf8') + '\',\'' +  dict[5].decode('utf8') + '\',\'' +  dict[6].decode('utf8')
    sqlStr += '\',\'' + dict[7].decode('utf8') + '\')'
      
    #sqlStr = 'insert into gua values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % (dict['gualist'],dict['name'],dict[0],dict[1],dict[2],dict[3],dict[4],dict[5],dict[6],dict[7])
    cur.execute(sqlStr)



tstr = linecache.getline(filepath,startline) 

#get qiangua
i = 0   
gua_dict['name'] = tstr
startline += 1
tstr = linecache.getline(filepath,startline)
gua_dict[i] = tstr
#print gua_dict[i].decode('utf8')
#print gua_dict['name'].decode('utf8')
while i<8: 
    startline += 1
    tstr = linecache.getline(filepath,startline) 
    print tstr.decode('utf8')                     
    if bGuaYaoYong(tstr,qiangua[i]):
        if i<6 :
            gua_dict['gualist'] += '1'
            gua_dict[i+1] = tstr
            i += 1
        elif i==6:
            gua_dict[i+1] = tstr
            i += 1
        elif i==7:
            #print tstr.decode('utf8')
            break
                 
insertGua(gua_dict)
initGua(gua_dict)


#get kungua
i = 0   
gua_dict['name'] = tstr
startline += 1
tstr = linecache.getline(filepath,startline)
gua_dict[i] = tstr
#print gua_dict[i].decode('utf8')
#print gua_dict['name'].decode('utf8')
while i<8: 
    startline += 1
    tstr = linecache.getline(filepath,startline)                   
    print tstr.decode('utf8')
    if bGuaYaoYong(tstr,kungua[i]):
        if i<6 :
            gua_dict['gualist'] += '0'
            gua_dict[i+1] = tstr
            i += 1
        elif i==6:
            gua_dict[i+1] = tstr
            i += 1
        elif i==7:
            #print tstr.decode('utf8')
            break
        #print tstr.decode('utf8')
insertGua(gua_dict)
initGua(gua_dict)

print linecount
#get 3-63gua
while(startline < linecount-1):
    print startline 
    i = 0   
    gua_dict['name'] = tstr
    startline += 1
    tstr = linecache.getline(filepath,startline)
    gua_dict[i] = tstr
    #print gua_dict[i].decode('utf8')
    #print gua_dict['name'].decode('utf8')
    while i<7: 
        startline += 1
        tstr = linecache.getline(filepath,startline)                   
        if bGuaYaoYong(tstr,yanggua[i]):
            if i<6 :
                gua_dict['gualist'] += '1'
            elif i==6:
                #print tstr.decode('utf8')
                break
        elif bGuaYaoYong(tstr,yingua[i]):
            if i<6 :
                gua_dict['gualist'] += '0'
            elif i==6:
                break
        else:
            continue
        gua_dict[i+1] = tstr
        i += 1
        #print tstr.decode('utf8')
    insertGua(gua_dict)
    initGua(gua_dict)

 
conn.close() 

'''
for i in range(linecount):
    initGua()
    tstr = linecache.getline(filepath,i)
    if bGuaYaoYong(tstr,guastr):
        guaci += tstr
print chardet.detect(guaci)
print guaci.decode('utf-8')
'''