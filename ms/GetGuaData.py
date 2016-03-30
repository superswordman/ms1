from lib.msutils import *
import os
'''
'original_list':'',
'original_guaname':'',
'original_guacomments':'',
'converted_list':'',
'converted_guaname':'',
'converted_guacomments':'',
'major_comments':'',
'minor_comments':'',
'yong_comments':'',
'''

class GetGuaData():
    def GetDataFromGua(self,gualist):
        engine = CreateMysqlConn()
        metadata = MetaData(engine)
        table =Table('gua', metadata, autoload=True)
        sel = select([table],table.c.gua_list==gualist)#([id],whereclause=text("date = '1993-01-01"))
        result = sel.execute()
        str ='~~~~~~~~~~~~~~~~~~~~~~:\n\n'
        selfdata = result.fetchone()
        for col in selfdata:
            str += '~~~%s' % col
        
        return str

    def upload_avator(self,filepath):
        return os.system(filepath)

    