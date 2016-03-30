from lib.msutils import *
class DelDataLibrary():
    def DelDayan1Data(self,stickid,index,ktype,startdate,enddate):
        if ktype:
            t_name = GetDayan1Tname(stickid,index,ktype)
        else:
            t_name = GetBaseDayan1Tname(stickid,index)
        engine = CreateMysqlConn()
        DelFromTable(engine,t_name,startdate,enddate)

    def DelStickData(self,stickid,index,ktype,startdate,enddate):
        if ktype:
            t_name = GetStickTname(stickid,index,ktype)
        else:
            t_name = GetBaseStickTname(stickid,index)
        engine = CreateMysqlConn()
        DelFromTable(engine,t_name,startdate,enddate)

#test = DelDataLibrary()
#test.DelDayan1Data('000001',True,'W','2016-02-20','2016-03-30')