from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
import datetime
import time

zsDict = {'000001':'sh','399001':'sz','399005':'zxb','399006':'cyb'}

def intTo2Str(num, digit):
    str = bin(num).replace('0b','')
    strhead = ''
    if len(str) < digit :
        for i in range(digit - len(str)):
            strhead += '0'

    return '%s%s' % (strhead, str) 

def CreateMysqlConn(user='msuser',password='ms123456',ip='localhost',port=3306,database='ms',charset='utf8'):
    ConnectStr = 'mysql://%s:%s@%s:%d/%s?charset=%s' % (user,password,ip,port,database,charset)
    return create_engine(ConnectStr)

def CleanTable(engine,tname):
    metadata = MetaData(engine)
    table =Table(tname, metadata, autoload=True)
    delete(table).execute()

def DelFromTable(engine,tname,startdate,enddate):
    metadata = MetaData(engine)
    table =Table(tname, metadata, autoload=True)
    delete(table,and_(table.c.date>=startdate,table.c.date<=enddate)).execute()
    #sel = delete(table).excute(and_(table.c.date>=startdate,
    #                        table.c.date<=enddate))
    #table.delete(and_(table.c.date>=startdate,table.c.date<=enddate))


def GetDayan1Tname(stickid,index,ktype):
    if index:
        t_name = 'dayan1_data_zs%s_' % (stickid)
    else :
        t_name = 'dayan1_data_%s_' % (stickid)

    t_name += GetPrefix(ktype)

    return t_name

def GetStickTname(stickid,index,ktype):
    if index:
        t_name = 'stick_data_zs%s_' % (stickid)
        print str(index)
    else :
        t_name = 'stick_data_%s_' % (stickid)

    t_name += GetPrefix(ktype)

    print 'GetStickTname:%s' % t_name
    return t_name

def GetPrefix(ktype):
    if ktype=='D':
        prefix_name = 'daily'
    elif ktype=='W':
        prefix_name = 'weekly'
    elif ktype=='M':
        prefix_name = 'monthly'
    #elif ktype=='120':
    #    prefix_name += '120'
    elif ktype=='60':
        prefix_name = '60'
    elif ktype=='30':
        prefix_name = '30'
    elif ktype=='15':
        prefix_name = '15'        
    elif ktype=='5':
        prefix_name = '5'
    else:
        prefix_name = 'base'

    return prefix_name

def GetBaseDayan1Tname(stickid,index):
    if index:
        t_name = 'dayan1_data_zs%s_base' % (stickid)
    else :
        t_name = 'dayan1_data_%s_base' % (stickid)

    return t_name

def GetBaseStickTname(stickid,index):
    if index:
        t_name = 'stick_data_zs%s_base' % (stickid)
    else :
        t_name = 'stick_data_%s_base' % (stickid)

    return t_name






