from __future__ import division 

from sqlalchemy import *
from lib.msutils import *

#coding=utf-8 
import Queue
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
shcsvfile = 'C:\Users\kai\Desktop\mysql\sh000001.csv'
#ds = ts.get_today_all()
#ds.to_csv(shcsvfile)
'''
zhishu
http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml?year=2016&jidu=1
gegu
http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000001.phtml?year=1991&jidu=4

#ds = ts.get_h_data('600449','2003-08-29','2016-02-06')
#ds = ts.get_hist_data('sh','1990-12-19','1990-12-20')
#ds = ts.get_hists({'sh'},'1990-01-01','2016-02-06')
#engine = create_engine('mysql://root:@127.0.0.1/ms?charset=utf8')
#df.to_sql('tick_data',engine)
#ds = ts.get_hists('sh','1990-01-01','2016-02-06')
#ds = ts.get_index()
#engine = create_engine('mysql://msuser:ms123456@localhost:3306/ms?charset=utf8',echo=True)

#print engine.execute('select * from gua;')
#ds.to_sql('tick_data_600449_daily',engine,if_exists='append')
#engine.close()

class Dayan1(object):
    __tablename__ = '_daily_dayan1'

    date= Column(DateTime, unique = True)
    original_list = Column(String)
    converted_list = Column(String)
    major_comments = Column(String)
    minor_comments = Column(String)  

    def __init__(self, date, original_list,converted_list,major_comments,minor_comments):
        self.date = date
        self.original_list = original_list
        self.converted_list = converted_list
        self.major_comments = major_comments
        self.minor_comments = minor_comments
     
    def __repr__(self):
        return "<Dayan1('%s','%s','%s','%s','%s')>" \
            % (self.date,self.original_list,self.converted_list,self.major_comments,self.minor_comments)  

'''

class Dayan1Library():

    def CreateDayan1Table(self,engine,tname,stickid):
        metadata=MetaData(engine)
        dayan1_table = Table(tname,metadata,
                   Column('id',Integer,primary_key = True,autoincrement=True),
                   Column('date',DateTime,unique = True),
                   Column('original_list',String(8)),
                   Column('original_guaname',String(20)),
                   Column('original_guacomments',String(256)),
                   Column('converted_list',String(8)),
                   Column('converted_guaname',String(20)),
                   Column('converted_guacomments',String(256)),
                   Column('major_comments',String(256)),
                   Column('minor_comments',String(256)),
                   Column('yong_comments',String(256)),
                   Column('open',Float),
                   Column('high',Float),
                   Column('close',Float),
                   Column('low',Float),
                   Column('volume',Float),
                   Column('amount',Float)
                   )
        metadata.create_all(engine)
        #dayan1_table = Table(tname,metadata,autoload=True)
        return dayan1_table

    def GetTickDataByDate(self,table,startdate,enddate):
        sel = select([table],and_(table.c.date>=startdate,table.c.date<=enddate)).order_by(table.c.date)#([id],whereclause=text("date = '1993-01-01"))
        result = sel.execute()
        return result.fetchall()

    def CloseMysqlConn(self,engine):
        engine.close()

    def GetYao(self,yesterdayclose,todayopen,todayclose):
        i1 = i2 = i3 = 0
        if(todayopen - yesterdayclose) < 0 :
            i1 = 0
        else:
            i1 = 1
        
        if (todayclose - todayopen) < 0:
            i2 = 0
        else:
            i2 = 1
        
        if (todayclose - yesterdayclose) < 0:
            i3 = 0
        else:
            i3 = 1

        return i1+i2+i3

    def GetDelta(self,yesterdayclose,todayopen,todayhigh,todayclose,todaylow,yesterdayvol,todayvol,yesterdayamount,todayamount):
        deltalist = {'open':0.0,'high':0.0,'close':0.0,'low':0.0,'volume':0,'amount':0}
            
        try:
            deltalist['open'] = round((todayopen - yesterdayclose)/yesterdayclose*100,2)
            deltalist['high'] = round((todayhigh - yesterdayclose)/yesterdayclose*100,2)
            deltalist['close'] = round((todayclose - yesterdayclose)/yesterdayclose*100,2)
            deltalist['low'] = round((todaylow - yesterdayclose)/yesterdayclose*100,2)
            deltalist['volume'] = round((todayvol - yesterdayvol)/yesterdayvol*100,2)
            deltalist['amount'] = round((todayamount - yesterdayamount)/yesterdayamount*100,2)
        except Exception as err:  
            print(err)  
        return deltalist

    def GetResultByDayan(self,yaolist,dongyaolist):
        dayanresult = {'converted_list':'','major_yaoid':-1,'minor_yaoid':-1,'yong':False}
        yaolen = len(dongyaolist)
        if yaolen == 1:#1 dongyao,use dongyao
            dayanresult['major_yaoid'] = dongyaolist[0]
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
        elif yaolen == 2:#2 dongyao,use last dongyao as major,first dongyao as minor
            dayanresult['major_yaoid'] = dongyaolist[1]
            dayanresult['minor_yaoid'] = dongyaolist[0]
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
        elif yaolen == 3:#3 dognyao,use converted_gua as major,original_gua as minor
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
        elif yaolen == 4:#4 dongyao,use first jingyao of converted_gua as major,last jingyao of converted_gua as minor
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
            jingyaolist = []
            for i in range(6):
                if i not in dongyaolist:
                    jingyaolist.append(i)
            dayanresult['major_yaoid'] = jingyaolist[0]
            dayanresult['minor_yaoid'] = jingyaolist[1]
        elif yaolen == 5:#5 dongyao,use jingyao of converted_gua
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
            jingyaolist = []
            for i in range(6):
                if i not in dongyaolist:
                    jingyaolist.append(i)
            dayanresult['major_yaoid'] = jingyaolist[0]
        elif yaolen == 6:#6 dongyao,use converted_gua
            dayanresult['converted_list'] = self.CreateConvertedList(yaolist,dongyaolist,yaolen)
            dayanresult['yong'] = True
        return dayanresult

    def GetGuaData(self,table,gua_list):
        sel = select([table],table.c.gua_list==gua_list)#([id],whereclause=text("date = '1993-01-01"))
        #sel1 = table.select(table.c.gua_list==gua_list)
        #execute(sel)
        #print str(sel)
        result = sel.execute()
        return result.fetchall()
                
    def CreateConvertedList(self,yaostr,dongyaolist,dongyaonum):
        xorlist = ['0','0','0','0','0','0']
        for i in range(dongyaonum):
            xorlist[dongyaolist[i]] = '1'
        xors = ''.join(xorlist)
        return intTo2Str(int(yaostr,2)^int(xors,2),6)


    def CreateDayan1Data(self,stickid,startdate,enddate,index,ktype):
        '''
        get a stick data,then insert data to mysql
        :param stickid :the stick id,eg:600449,if get zhishu,please use 'sh'(sh000001)

        :param startdate:the stick startdate,eg:'1990-01-01',must be valid

        :param enddate:the stick enddate,eg:'1990-01-01'

        '''
        print '%s,%s' % (index,type(index))
        if ktype :
            stick_t_name = GetStickTname(stickid,index,ktype)
            dayan1_t_name = GetDayan1Tname(stickid,index,ktype)
        else :
            stick_t_name = GetBaseStickTname(stickid,index)
            dayan1_t_name = GetBaseDayan1Tname(stickid,index)
        
        engine = CreateMysqlConn()
        dayan1Table = self.CreateDayan1Table(engine,dayan1_t_name,stickid)

        dayan1_tempt_name = dayan1_t_name+'_temp'
        dayan1TempTable = self.CreateDayan1Table(engine,dayan1_tempt_name,stickid)
        '''
        
        metadata=MetaData(engine)
        dayan1Table = Table(dayan1_t_name,metadata,
                   Column('id',Integer,unique = True,autoincrement=True),
                   Column('date',DateTime,unique = True),
                   Column('original_list',String(8)),
                   Column('original_guaname',String(20)),
                   Column('original_guacomments',String(256)),
                   Column('converted_list',String(8)),
                   Column('converted_guaname',String(20)),
                   Column('converted_guacomments',String(256)),
                   Column('major_comments',String(256)),
                   Column('minor_comments',String(256)),
                   Column('yong_comments',String(256)),
                   Column('open',Float(4,2)),
                   Column('high',Float(4,2)),
                   Column('close',Float(4,2)),
                   Column('low',Float(4,2))
                   )
        metadata.create_all(engine)
        #dayan1Table = Table(dayan1_t_name,metadata,autoload=True)
        '''

        TickMetadata = MetaData(engine)
        start_date = datetime.datetime.strptime(startdate,'%Y-%m-%d')
        end_date = datetime.datetime.strptime(enddate,'%Y-%m-%d')
        try:
            TickdataTable =Table(stick_t_name, TickMetadata, autoload=True)        
            result = self.GetTickDataByDate(TickdataTable,start_date,end_date)
        except  Exception as err:  
            print(err) 
            return
        
        Guametadata = MetaData(engine)
        Guatable = Table('gua',Guametadata,autoload=True)
        basequeue = []
        for row in result:           
            if len(basequeue) < 7 :
                basequeue.append(row)
            else :
                insertdata = {'date':'',
                   'original_list':'',
                   'original_guaname':'',
                   'original_guacomments':'',
                   'converted_list':'',
                   'converted_guaname':'',
                   'converted_guacomments':'',
                   'major_comments':'',
                   'minor_comments':'',
                   'yong_comments':'',
                   'open':0.0,
                   'high':0.0,
                   'close':0.0,
                   'low':0.0,
                   'volume':0.0,
                   'amount':0.0
                   }
                yaolist = ''
                transyaoid = []
                #get dongyao
                for i in range(6):
                    yaonum = self.GetYao(basequeue[i][4],basequeue[i+1][2],basequeue[i+1][4])
                    if yaonum < 2:
                        yaolist += '0'
                        if yaonum == 0:
                            transyaoid.append(i)
                    else :
                        yaolist += '1'
                        if yaonum == 3:
                            transyaoid.append(i)
                #create table data
                insertdata['date'] = row[1]
                ogrigirow = self.GetGuaData(Guatable,yaolist)
                insertdata['original_list'] = ogrigirow[0][0]
                insertdata['original_guaname'] = ogrigirow[0][1]
                #print ogrigirow[0][1]
                insertdata['original_guacomments'] = ogrigirow[0][2]                

                dayanres = self.GetResultByDayan(yaolist,transyaoid)
                if len(dayanres['converted_list']) > 0:
                    convertedrow = self.GetGuaData(Guatable,dayanres['converted_list'])
                    insertdata['converted_list'] = convertedrow[0][0]
                    insertdata['converted_guaname'] = convertedrow[0][1]
                    insertdata['converted_guacomments'] = convertedrow[0][2]                
                    if len(transyaoid) > 3:
                        if dayanres['major_yaoid'] >= 0:
                            insertdata['major_comments'] = convertedrow[0][dayanres['major_yaoid']+3]
                        if dayanres['minor_yaoid'] >= 0:
                            insertdata['minor_comments'] = convertedrow[0][dayanres['minor_yaoid']+3]
                        if dayanres['yong'] == True:
                            if (dayanres['converted_list'] == '000000') or (dayanres['converted_list'] == '111111'):
                                insertdata['yong_comments'] = convertedrow[0][9]
                            else :
                                insertdata['yong_comments'] = convertedrow[0][2]
                    elif len(transyaoid) < 3:
                        if dayanres['major_yaoid'] >= 0:
                            insertdata['major_comments'] = ogrigirow[0][dayanres['major_yaoid']+3]
                        if dayanres['minor_yaoid'] >= 0:
                            insertdata['minor_comments'] = ogrigirow[0][dayanres['minor_yaoid']+3]

                #get delta data
                delta = self.GetDelta(basequeue[6][4],
                                      row[2],
                                      row[3],
                                      row[4],
                                      row[5],
                                      basequeue[6][6],
                                      row[6],
                                      basequeue[6][7],
                                      row[7])
                insertdata['open'] = delta['open'] 
                insertdata['high'] = delta['high'] 
                insertdata['close'] = delta['close'] 
                insertdata['low'] = delta['low']  
                insertdata['volume'] = delta['volume'] 
                insertdata['amount'] = delta['amount']  
                #print insertdata['open']
                '''
                ins = dayan1Table.insert().values(date=insertdata['date'],
                                         original_list=insertdata['original_list'],
                                         original_guaname=insertdata['original_guaname'],
                                         original_guacomments=insertdata['original_guacomments'],
                                         converted_list=insertdata['converted_list'],
                                         converted_guaname=insertdata['converted_guaname'],
                                         converted_guacomments=insertdata['converted_guacomments'],
                                         major_comments=insertdata['major_comments'],
                                         minor_comments=insertdata['minor_comments'],
                                         yong_comments=insertdata['yong_comments'],
                                         open=insertdata['open'],
                                         high=insertdata['high'],
                                         close=insertdata['close'],
                                         low=insertdata['low'])
                '''
                try:
                    ins = insert(dayan1Table).execute(date=insertdata['date'],
                                         original_list=insertdata['original_list'],
                                         original_guaname=insertdata['original_guaname'],
                                         original_guacomments=insertdata['original_guacomments'],
                                         converted_list=insertdata['converted_list'],
                                         converted_guaname=insertdata['converted_guaname'],
                                         converted_guacomments=insertdata['converted_guacomments'],
                                         major_comments=insertdata['major_comments'],
                                         minor_comments=insertdata['minor_comments'],
                                         yong_comments=insertdata['yong_comments'],
                                         open=insertdata['open'],
                                         high=insertdata['high'],
                                         close=insertdata['close'],
                                         low=insertdata['low'],
                                         volume=insertdata['volume'],
                                         amount=insertdata['amount'])
                except Exception as err:  
                    print(err)  
                    #print str(ins)
                #excute(ins)
                #create new queue
                del basequeue[0]
                basequeue.append(row)   
        
        #insert to temp table
        print "insert tmp data``````````````````````````````````````````````````````````````"
        insertdata = {'date':'',
                   'original_list':'',
                   'original_guaname':'',
                   'original_guacomments':'',
                   'converted_list':'',
                   'converted_guaname':'',
                   'converted_guacomments':'',
                   'major_comments':'',
                   'minor_comments':'',
                   'yong_comments':'',
                   'open':0.0,
                   'high':0.0,
                   'close':0.0,
                   'low':0.0,
                   'volume':0.0,
                   'amount':0.0
                   }
        yaolist = ''
        transyaoid = []
        #del basequeue[0]
        #basequeue.append(row)
        for i in range(6):
            yaonum = self.GetYao(basequeue[i][4],basequeue[i+1][2],basequeue[i+1][4])
            if yaonum < 2:
                yaolist += '0'
                if yaonum == 0:
                    transyaoid.append(i)
            else :
                yaolist += '1'
                if yaonum == 3:
                    transyaoid.append(i)
            #create table data
        insertdata['date'] = basequeue[6][1]
        ogrigirow = self.GetGuaData(Guatable,yaolist)
        insertdata['original_list'] = ogrigirow[0][0]
        insertdata['original_guaname'] = ogrigirow[0][1]
        #print ogrigirow[0][1]
        insertdata['original_guacomments'] = ogrigirow[0][2]                

        dayanres = self.GetResultByDayan(yaolist,transyaoid)
        if len(dayanres['converted_list']) > 0:
            convertedrow = self.GetGuaData(Guatable,dayanres['converted_list'])
            insertdata['converted_list'] = convertedrow[0][0]
            insertdata['converted_guaname'] = convertedrow[0][1]
            insertdata['converted_guacomments'] = convertedrow[0][2]                
            if len(transyaoid) > 3:
                if dayanres['major_yaoid'] >= 0:
                    insertdata['major_comments'] = convertedrow[0][dayanres['major_yaoid']+3]
                if dayanres['minor_yaoid'] >= 0:
                    insertdata['minor_comments'] = convertedrow[0][dayanres['minor_yaoid']+3]
                if dayanres['yong'] == True:
                    if (dayanres['converted_list'] == '000000') or (dayanres['converted_list'] == '111111'):
                        insertdata['yong_comments'] = convertedrow[0][9]
                    else :
                        insertdata['yong_comments'] = convertedrow[0][2]
            elif len(transyaoid) < 3:
                if dayanres['major_yaoid'] >= 0:
                    insertdata['major_comments'] = ogrigirow[0][dayanres['major_yaoid']+3]
                if dayanres['minor_yaoid'] >= 0:
                    insertdata['minor_comments'] = ogrigirow[0][dayanres['minor_yaoid']+3]


        #get delta data
        delta = self.GetDelta(basequeue[6][4],
                                row[2],
                                row[3],
                                row[4],
                                row[5],
                                basequeue[6][6],
                                row[6],
                                basequeue[6][7],
                                row[7])
        insertdata['open'] = delta['open'] 
        insertdata['high'] = delta['high'] 
        insertdata['close'] = delta['close'] 
        insertdata['low'] = delta['low']  
        insertdata['volume'] = delta['volume'] 
        insertdata['amount'] = delta['amount']  

        try:
            ins = insert(dayan1TempTable).execute(date=insertdata['date'],
                                    original_list=insertdata['original_list'],
                                    original_guaname=insertdata['original_guaname'],
                                    original_guacomments=insertdata['original_guacomments'],
                                    converted_list=insertdata['converted_list'],
                                    converted_guaname=insertdata['converted_guaname'],
                                    converted_guacomments=insertdata['converted_guacomments'],
                                    major_comments=insertdata['major_comments'],
                                    minor_comments=insertdata['minor_comments'],
                                    yong_comments=insertdata['yong_comments'],
                                    open=insertdata['open'],
                                    high=insertdata['high'],
                                    close=insertdata['close'],
                                    low=insertdata['low'],
                                    volume=insertdata['volume'],
                                    amount=insertdata['amount'])
        except Exception as err:  
            print(err)  
        
        #get start id
        '''
        sel = select([TickdataTable.c.id],TickdataTable.c.date>=start_date,)#([id],whereclause=text("date = '1993-01-01"))
        result = sel.execute()
        startid = result.fetchone()[0]
        
        sel = select([TickdataTable.c.id],TickdataTable.c.date==end_date)#([id],whereclause=text("date = '1993-01-01"))
        result = sel.execute()
        endid = result.fetchone()[0]

        idrange = endid - startid
        for i in range(idrange):
            rol = GetTickDataById(TickdataTable, startid+i-7)    
        #self.CloseMysqlConn(engine)
        '''
#testc = Dayan1Library()
#testc.CreateDayan1Data('000001','2001-02-04','2016-03-29',True,'W')