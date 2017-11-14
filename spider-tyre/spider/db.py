# -*- coding: utf-8
import MySQLdb
import self as self

from config import *

class ConnectDB(object):
    def __init__(self):
		self.db=MySQLdb.connect(DB_HOST,DB_USER,PASSWORD,DB_NAME,charset="utf8")   #连接数据库
		self.cursor = self.db.cursor()

    def select(self,table_name="",field="",value=""):
		sql=''' select %s from %s where %s = \'%s\' ''' % (field,table_name,field,value)
		result=self.cursor.execute(sql)
		return result

    def insert(self,table_name="",
               tyreid = "",
               brand="",
               streak="",
               name="",
               standard="",
               loaded="",
               speed="",
               wearproof="",
               traction="",
               highTemperature=""):
            sql = '''insert into %s set
                    tyreID = \'%s\',
                    brand =  \'%s\',
                    streak= \'%s\',
                    name= \'%s\',
                    standard= \'%s\',
                    loaded=\'%s\',
                    speed=\'%s\',
                    wearproof=\'%s\',
                    traction=\'%s\',
                    highTemperature=\'%s\'
                            ''' %(table_name,
                                  tyreid,
                                  brand,
                                  streak,
                                  name,
                                  standard,
                                  loaded,
                                  speed,
                                  wearproof,
                                  traction,
                                  highTemperature
                                  )
            self.cursor.execute(sql)
            self.db.commit()

    def dbclose(self):
		self.db.close()