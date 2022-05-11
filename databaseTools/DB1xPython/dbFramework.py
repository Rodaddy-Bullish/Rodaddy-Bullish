import sys
import time
import psycopg2
import psycopg2 as postgres
from psycopg2 import OperationalError, errorcodes, errors

USER = 'rrojas@b1ops.net'


class SetupDb(object):
    
    def __init__(self,
                 dbHost='127.0.0.1',
                 dbUser='USER',
                 database='',
                 dbPort=None
                 ):
        
        self.dbHost = dbHost
        self.dbUser = dbUser
        self.database = database
        self.dbPort = str(dbPort)
    
    def connect(self, retries=2):
        
        conString = f"dbname={self.database} user={self.dbUser} host='127.0.0.1' password='' port={self.dbPort}"
        while retries:
            try:
                connection = postgres.connect(conString)
                return connection
            except psycopg2.errors as e:
                print("Connection failed.  sleeping 1 sec for proxy to set")
                time.sleep(1)
                retries -= 1
        
        print(f"tried to reconenct 2 times, please make sure Proxy is up for \n{conString}")
        sys.exit(2)

    def execute(self, sql):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            connection.autocommit(False)
            cursor.execute(sql)
            connection.commit()
            connection.close()
        
        except psycopg2.Error as e:
            print("ERROR: SQL execution failed: %s" % str(e))
            print("SQL: %s" % sql)
            print("execution failed: %s" % e)
            sys.exit(2)
    
    def fetchOne(self, sql):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            resultSet = cursor.fetchone()
            connection.close()
            return resultSet
        
        except psycopg2.Error as e:
            print("ERROR: SQL fetchone failed: %s" % str(e))
            print("SQL: %s" % sql)
            print("fetchall failed, \n %s" % str(e))
            sys.exit(2)
    
    def fetchOneDict (self, sql, index=None):
        resultSet = False
        
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            resultSet = cursor.fetchone()
            connection.close()
        
        except psycopg2.Error as e:
            print("ERROR: SQL fetchonedict failed: %s" % str(e))
            print("SQL: %s" % sql)
            print("fetchall failed, \n %s" % e)
            sys.exit(2)
        
        if resultSet:
            if not index:
                return resultSet
            else:
                tempDict = {}
                try:
                    tempDict[resultSet[index]] = resultSet
                    
                except IndexError as e:
                    print(f"issue inserting index:{index}")
                    print("Either try not using an index or a different method")
                    sys.exit(2)
                    
                return tempDict
    
    def fetchAll(self, sql: str) -> object:
        
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            resultSet = cursor.fetchall()
            connection.close()
            return resultSet
        
        except Exception as e:
            print("ERROR: SQL fetchAll failed: %s" % str(e))
            print("SQL: %s" % sql)
            print("fetchall failed, \n %s" % e)
            sys.exit(2)
    
    def fetchAllDict(self, sql, index=None):
        
        resultSet = False
        
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            resultSet = cursor.fetchall()
            connection.close()
        
        except Exception as e:
            errorStr = "ERROR: SQL fetchone failed: %s" % str(e)
            print(errorStr)
            print("SQL: %s" % sql)
            print("fetchall failed, \n %s" % str(e))
            sys.exit(2)
        
        if resultSet:
            if not index:
                return resultSet
            else:
                rsDict = {}
                for row in resultSet:
                    try:
                        rsDict[row[index]] = row
                    except:
                        pass
                return rsDict
        else:
            print("NO RESULTS: %s" % sql)
            return None
    
    def fetchAllList(self, sql, index=None):
        
        resultSet = None
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            resultSet = cursor.fetchall()
            connection.close()
        
        except Exception as e:
            print("ERROR: SQL fetchAllList failed: %s" % str(e))
            print("SQL: %s" % sql)
            print("fetch all dict failed")
            sys.exit(2)
        
        if resultSet:
            if not index:
                return resultSet
            else:
                outList = []
                for row in resultSet:
                    try:
                        outList.append(row[index])
                    except:
                        print(f"issue inserting index:{index} for row: {row}")
                        sys.exit(3)
            return outList
