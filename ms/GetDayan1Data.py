from lib.msutils import *
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

class GetDayan1Data():
    def GetDataByDate(self,stickid,date,index,ktype):
        engine = CreateMysqlConn()
        dayan1Metadata = MetaData(engine)
        date = datetime.datetime.strptime(date,'%Y-%m-%d  %H:%M:%S')
        if ktype:
            t_name = GetDayan1Tname(stickid,index,ktype)
        else:
            t_name = GetBaseDayan1Tname(stickid,index)
        
        table =Table(t_name, dayan1Metadata, autoload=True)
        sel = select([table],table.c.date==date)#([id],whereclause=text("date = '1993-01-01"))
        result = sel.execute()
        str = ''
        #str ='~~~~~~~~~~~selfdata~~~~~~~~~~~:\n\n'
        selfdata = result.fetchone()
        #for col in selfdata:
        #    str += '~~~  %s  ' % col
        
        #check whether yong exist
        if not selfdata :
            return 'no data'

        if len(selfdata[10])>0:
            #1th data
            sel = select([table],table.c.yong_comments==selfdata[10])
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '                 ~~~~~~~~~~~\n\n'
            '''
            #2th data
            sel = select([table],and_(table.c.yong_comments!=selfdata[10],
                                          table.c.major_comments=='',
                                          table.c.converted_list==selfdata[5]))
            result = sel.execute()
            if result:
                str ='\n~~~~~~~~~~~2th data~~~~~~~~~~~\n\n'
                tdata = result.fetchall()
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
            '''
            return str

        #check whether major exist
        if len(selfdata[8])>0 :
            #1th data
            sel = select([table],and_(table.c.minor_comments==selfdata[9],
                                          table.c.major_comments==selfdata[8],
                                          table.c.converted_list==selfdata[5],
                                          table.c.original_list==selfdata[2]))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
            
            '''
            #2th data
            sel = select([table],and_(table.c.minor_comments==selfdata[9],
                                          table.c.major_comments==selfdata[8],
                                          table.c.converted_list!=selfdata[5],
                                          table.c.original_list!=selfdata[2]))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~2th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
          
            #3th data
            sel = select([table],and_(table.c.minor_comments!=selfdata[9],
                                      table.c.major_comments==selfdata[8],
                                      table.c.converted_list!=selfdata[5],
                                      table.c.original_list!=selfdata[2]))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~3th data~~~~~~~~~~~:\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~:\n\n'
            '''
            return str

        #check whether converted exist
        if len(selfdata[5])>0 :
            #1th data
            sel = select([table],and_(table.c.minor_comments==selfdata[9],
                                          table.c.major_comments==selfdata[8],
                                          table.c.converted_list==selfdata[5],
                                          table.c.original_list==selfdata[2]))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
            '''
            #2th data
            sel = select([table],and_(table.c.converted_list==selfdata[5],
                                      table.c.original_list!=selfdata[2],
                                      table.c.minor_comments=='',
                                      table.c.major_comments==''))
            result = sel.execute()
            if result:
                str ='\n~~~~~~~~~~~2th data~~~~~~~~~~~\n\n'
                tdata = result.fetchall()
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '                 ~~~~~~~~~~~\n\n'
            '''
            return str

        #check whether original exist
        if len(selfdata[2])>0 :
            #1th data
            sel = select([table],and_(table.c.minor_comments==selfdata[9],
                                          table.c.major_comments==selfdata[8],
                                          table.c.converted_list==selfdata[5],
                                          table.c.original_list==selfdata[2]))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
            return str
        
        return str

    def GetDataByGua(self,stickid,index,ktype,original='',converted=''):
        #print '%s,%s,%s,%s,%s,%s,%s,%s' % (stickid,index,ktype,original,converted,major,minor,yong)
        #major = major.encode('utf8')
        engine = CreateMysqlConn()
        dayan1Metadata = MetaData(engine)
        if ktype:
            t_name = GetDayan1Tname(stickid,index,ktype)
        else:
            t_name = GetBaseDayan1Tname(stickid,index)
        table =Table(t_name, dayan1Metadata, autoload=True)
        str = ''
        #print len(converted)
 
                        #check whether converted exist
        if len(converted)>0 :
            #print 'start converted'
            #1th data
            sel = select([table],and_(table.c.converted_list==converted,
                                          table.c.original_list==original))
            result = sel.execute()
            tdata = result.fetchall()
            #print tdata
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
           
            '''
            #2th data
            sel = select([table],and_(table.c.converted_list==converted,
                                      table.c.original_list!=original))
            result = sel.execute()
            if result:
                str +='\n~~~~~~~~~~~2th data~~~~~~~~~~~\n\n'
                tdata = result.fetchall()
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '                 ~~~~~~~~~~~\n\n'
            '''
            return str
        
        #check whether original exist
        if len(original)>0 :
            #1th data
            sel = select([table],and_(table.c.converted_list==converted,
                                      table.c.original_list==original))
            result = sel.execute()
            tdata = result.fetchall()
            if tdata:
                str +='\n\n~~~~~~~~~~~1th data~~~~~~~~~~~\n\n'
                for row in tdata:
                    for col in row:
                        str += '~~~  %s  ' % col
                    str += '\n\n                 ~~~~~~~~~~~\n\n'
            return str
        
        return str




#test = GetDayan1Data()
#print test.GetDataByDate('000001','2015-06-19',indext=True)
#print test.GetDataByGua('000001',True,'','010110','100101')