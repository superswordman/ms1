import tushare as ts
from tushare import *
from lib.msutils import *
import pandas
#coding=utf-8 
import linecache
import os
import chardet
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )
zsDict = {'000001':'sh','399001':'sz','399005':'zxb','399006':'cyb'}
#ds = ts.get_today_all()
#ds.to_csv(shcsvfile)
'''
zhishu
http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml?year=2016&jidu=1
gegu
http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000001.phtml?year=1991&jidu=4

ds = ts.get_h_data('600449','2003-08-29','2016-02-06')
#ds = ts.get_hist_data('sh','1990-12-19','1990-12-20')
#ds = ts.get_hists({'sh'},'1990-01-01','2016-02-06')
#engine = create_engine('mysql://root:@127.0.0.1/ms?charset=utf8')#存入数据库
#df.to_sql('tick_data',engine)
#ds = ts.get_hists('sh','1990-01-01','2016-02-06')
#ds = ts.get_index()
engine = create_engine('mysql://msuser:ms123456@localhost:3306/ms?charset=utf8',echo=True)
ts.get_hists('sh','1990-01-01','2016-02-06')
#print engine.execute('select * from gua;')
#存入数据库
ds.to_sql('tick_data_600449_daily',engine,if_exists='append')
engine.close()
'''
#pandas.DataFrame.sort(
#ds = ts.get_h_data('000001','2003-08-29','2003-09-06',index=True)
#engine = create_engine('mysql://msuser:ms123456@localhost:3306/ms?charset=utf8',echo=True)
#ds.sort_index(ascending=True).to_sql('tick_data_sh_daily',engine,if_exists='append')

class StickdataLibrary():
    def GetTickData(self,stickid,startdate,enddate,indext,ktypet):
        print type(indext)
        if indext:
            id = zsDict[stickid]
        else:
            id = stickid
        print "stickid:%s,ktypet:%s" % (id,ktypet)
        try:
            ds = ts.get_hist_data(id,startdate,enddate,ktype=ktypet)
        except Exception as err:  
            print(err)  
        print "GetTickData end!"
        return ds
    
    def GetBaseTickData(self,stickid,startdate,enddate,indext):
        try:
            ds = ts.get_h_data(stickid,startdate,enddate,index=indext)
        except Exception as err:  
            print(err)  

        return ds
    #.sort(columns='date')

    def InsertTickData(self,engine,stickid,dataFrame,index,ktype):
        t_name = GetStickTname(stickid,index,ktype)        
        print t_name
        metadata = MetaData(engine)
        if index:
            Table(t_name,metadata,
                        Column('id',Integer,primary_key = True,autoincrement=True),
                        Column('date',DateTime,unique = True),
                        Column('open',DOUBLE),
                        Column('high',DOUBLE),
                        Column('close',DOUBLE),
                        Column('low',DOUBLE),
                        Column('volume',DOUBLE),
                        Column('price_change',DOUBLE),
                        Column('p_change',DOUBLE),
                        Column('ma5',DOUBLE),
                        Column('ma10',DOUBLE),
                        Column('ma20',DOUBLE),
                        Column('v_ma5',DOUBLE),
                        Column('v_ma10',DOUBLE),
                        Column('v_ma20',DOUBLE)
                        )
            print 'index:True'
        else:
            Table(t_name,metadata,
                        Column('id',Integer,primary_key = True,autoincrement=True),
                        Column('date',DateTime,unique = True),
                        Column('open',DOUBLE),
                        Column('high',DOUBLE),
                        Column('close',DOUBLE),
                        Column('low',DOUBLE),
                        Column('volume',DOUBLE),
                        Column('price_change',DOUBLE),
                        Column('p_change',DOUBLE),
                        Column('ma5',DOUBLE),
                        Column('ma10',DOUBLE),
                        Column('ma20',DOUBLE),
                        Column('v_ma5',DOUBLE),
                        Column('v_ma10',DOUBLE),
                        Column('v_ma20',DOUBLE),
                        Column('turnover',DOUBLE)
                        )
            print 'index:False'

        metadata.create_all(engine)
        try:
            dataFrame.to_sql(t_name,engine,if_exists='append')
        except Exception as err:  
            print(err)  
            

    def InsertBaseTickData(self,engine,stickid,dataFrame,index):
        t_name = GetBaseStickTname(stickid,index)        
        
        metadata = MetaData(engine)

        Table(t_name,metadata,
                Column('id',Integer,primary_key = True,autoincrement=True),
                Column('date',DateTime,unique = True),
                Column('open',DOUBLE),
                Column('high',DOUBLE),
                Column('close',DOUBLE),
                Column('low',DOUBLE),
                Column('volume',DOUBLE),
                Column('amount',DOUBLE)
                )
        metadata.create_all(engine)
        try:
            dataFrame.to_sql(t_name,engine,if_exists='append')
        except Exception as err:  
            print(err)  

    def CloseMysqlConn(self,engine):
        engine.close()



    def CreateTickData(self,stickid,startdate,enddate,index,ktype):
        '''
        get a stick data,then insert data to mysql
        :param stickid :the stick id,eg:600449,if get zhishu,please use 'sh'(sh000001)

        :param startdate:the stick startdate,eg:'1990-01-01',must be valid

        :param enddate:the stick enddate,eg:'1990-01-01'

        :param index:if get zhishu,pleanse set index=True
        '''
        print '%s,%s,%s,%s' % (stickid,startdate,enddate,ktype)
        try:
            ds = self.GetTickData(stickid,startdate,enddate,index,ktype)
            engine = CreateMysqlConn()
            self.InsertTickData(engine,stickid,ds.sort_index(ascending=True),index,ktype)
        except Exception as err:  
            print(err)  

    def CreateBaseTickData(self,stickid,startdate,enddate,index):
        '''
        get a stick data,then insert data to mysql
        :param stickid :the stick id,eg:600449,if get zhishu,please use 'sh'(sh000001)

        :param startdate:the stick startdate,eg:'1990-01-01',must be valid

        :param enddate:the stick enddate,eg:'1990-01-01'

        :param index:if get zhishu,pleanse set index=True
        '''
        #print '%s,%s,%s,%s' % (stickid,startdate,enddate,index)
        try:
            ds = self.GetBaseTickData(stickid,startdate,enddate,index)
            engine = CreateMysqlConn()
            self.InsertBaseTickData(engine,stickid,ds.sort_index(ascending=True),index)
        except Exception as err:  
            print(err)  

#testtick = StickdataLibrary()
#testtick.CreateTickData('000001','2011-02-25','2016-03-14',True,'120')