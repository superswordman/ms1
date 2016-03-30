from lib.msutils import *
class CleanDataLibrary():
    def CleanDayan1Data(self,stickid,index,ktype):
        if ktype :
            dayan1_t_name = GetDayan1Tname(stickid,index,ktype)
        else :
            dayan1_t_name = GetBaseDayan1Tname(stickid,index)
       
        engine = CreateMysqlConn()
        CleanTable(engine,dayan1_t_name)

    def CleanStickData(self,stickid,index=False):
        if index:
            tick_t_name = 'tick_data_zs%s_daily' % (stickid)
        else :
            tick_t_name = 'tick_data_%s_daily' % (stickid)
        engine = CreateMysqlConn()
        CleanTable(engine,tick_t_name)

#test = CleanDataLibrary()
#test.CleanDayan1Data('000001',True,'30')