import os
from pickle import NONE
from sqlalchemy import create_engine
import pymysql
import pandas

class mysqldb:

    LOGGER = None
    CONFIG = None

    def __init__(self):
        #todo: raise error if config
        self.__config = mysqldb.CONFIG()
        self.connection = create_engine(self.__config.get_db_connection(), pool_recycle=3600)
        self.__connect()
        

    def __connect(self):
        h, u = self.__config.get("DATABASE.HOST"), self.__config.get("DATABASE.USER")
        p, db = self.__config.get("DATABASE.PASSWORD"), self.__config.get("DATABASE.DB_NAME")
        port = int(self.__config.get("DATABASE.PORT"))
        self.raw_connection = pymysql.connect(host=h, user=u, password=p, db=db, port=port)

    
    #execute insert query on table by using params(dictionary)
    def insert(self, data, tableName):
        if len(data) == 0: return True

        cursor = self.raw_connection.cursor()
        try:
            cols = ",".join(["`{0}`".format(l) for l in list(data[0].keys())])
            for d in data:
                query = "insert into {0}({1}) values{2}".format(tableName, cols, tuple(d.values()))
                query = query.replace("None", "NULL")
                cursor.execute(query)
            cursor.close()
            self.raw_connection.commit()
            return True
        except Exception as e:
            mysqldb.LOGGER.log("Exeception occured:{}".format(e))
            cursor.close()
            return False
            

    #execute stored procedure.
    def execute_sp(self, sp, params):
        cursor = self.raw_connection.cursor()
        try:                               
            cursor.execute("CALL {0}()".format(sp))
            res = cursor.fetchone()
            cursor.close()
            self.raw_connection.commit()
            return res[0] if len(res) > 0 else 0
        except Exception as e:
            mysqldb.LOGGER.log("Exeception occured:{}".format(e))
            cursor.close()
            return -1

    
    #execute script from a file.
    def execute(self, file, params):
        file = self.__config.get("COMMON.SQL_SCRIPTS") + file
        if not os.path.isfile(file): return False

        cursor = self.raw_connection.cursor()
        try:                               
            script = open(file,'r').read().format(**params)
            cursor.execute(script)
            cursor.close()
            self.raw_connection.commit()
            return True
        except Exception as e:
            mysqldb.LOGGER.log("Exeception occured:{}".format(e))
            cursor.close()
            return False
        
    
    #save pandas dataset to table.
    def save(self, dataset, tableName):
        if len(dataset) == 0: return True

        dbConnection = self.connection.connect()
        try:
            frame = dataset.to_sql(tableName, dbConnection, if_exists='append', index=False)
            dbConnection.close()
            mysqldb.LOGGER.log("Table %s is updated successfully." % tableName)
            return True
        except ValueError as vx:
            mysqldb.LOGGER.log(vx)
            dbConnection.close()
            return False
        except Exception as ex:   
            mysqldb.LOGGER.log(ex)
            dbConnection.close()
            return False
            

    #get table as pandas
    def get(self, query):
        dbConnection = self.connection.connect()
        try:
            frame = pandas.read_sql(query, dbConnection)
            dbConnection.close()
            return frame
        except Exception as ex:   
            mysqldb.LOGGER.log(ex)
            dbConnection.close()
            return None

    def getone(self, query):
        records = self.getall(query)
        return records[0] if len(records) > 0 else None

    
    #get list of records (dictionary format)
    def getall(self, query):
        try:
            cursor = self.raw_connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as ex:   
            mysqldb.LOGGER.log(ex)
            cursor.close()
            return []
            