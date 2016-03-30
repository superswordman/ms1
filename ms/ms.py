def test(a,b=True):
    print type(b)

#test(1,True)
'''
from sqlalchemy import *
#from sqlalchemy.orm import *
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )

def CreateMysqlConn(user='msuser',password='ms123456',ip='localhost',port=3306,database='ms',charset='utf8'):
    ConnectStr = 'mysql://%s:%s@%s:%d/%s?charset=%s' % (user,password,ip,port,database,charset)
    return create_engine(ConnectStr)

def CreateTable(engine,stickid,indext):
    print 'create table test'

def GetTickData(engine,stickid,date):
    SqlStr = 'select * from tick_data_%s_daily where date < %s order by date desc limit 6' % (stickid,date)
    return engine.excute(SqlStr)

engine = CreateMysqlConn()

#session.commit()
# 关闭session:
#session.close()

metadata=MetaData(engine)
user_table = Table('%s_daily_dayan1' % ('zs000001'),metadata,
                   Column('date',DATE,unique = True),
                   Column('original_list',String(8)),
                   Column('original_gua',String(20)),
                   Column('converted_list',String(8)),
                   Column('converted_gua',String(20)),
                   Column('major_comments',String(256)),
                   Column('minor_comments',String(256))
                   )
metadata.create_all(engine)
#print user_table.columns
TickMetadata = MetaData(engine)
TickdataTable =Table('tick_data_%s_daily' % ('zs000001'), TickMetadata, autoload=True)
#print TickdataTable.columns
#sel = select([TickdataTable.c.id],TickdataTable.c.date=='1991-01-01')#([id],whereclause=text("date = '1993-01-01"))
sel = select([TickdataTable.c.id],TickdataTable.c.date==datetime.date(1990,12,19))#([id],whereclause=text("date = '1993-01-01"))
result = sel.execute()
for row in result:
    print row[0]
#result = GetTickData(engine,'sh','2016-02-05')

#print result
'''