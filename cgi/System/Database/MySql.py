
import MySQLdb

class MySql:
        
    user = ''
    
    connection = ''
    
    queries = 0
    
    lastQuery = ''
    
    sessionObject = None
    
    def __init__(self, sessionObject):
        self.sessionObject = sessionObject
    
    def connect(self, host, user, password, port = 3306):
        #return True;
        self.connection = MySQLdb.connect(host = host, user = user, passwd = password, port = port)
        if(not self.connection):
            return False
        return True
        
    def query(self, query):
        self.queries += 1
        cursor = self.connection.cursor()
        
        self.lastQuery = query
        
        try:
            cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall();
        except MySQLdb.Error, e:
            try:                
                self.sessionObject.setNotice('alert', "MySQL Error "+str(e.args[0])+": <b>"+str(e.args[1])+"</b>")
            except IndexError:
                print "MySQL Error: %s" % str(e)
                self.sessionObject.setNotice('alert', "MySQL Error "+str(e))
                
        return False
        
    def getLastQuery(self):
        return self.lastQuery

    def getEngines(self):
        return self.query("SELECT * FROM `information_schema`.`ENGINES` ORDER BY `SUPPORT` ASC")
    
    def getCollations(self):
        return self.query("SELECT * FROM `information_schema`.`COLLATIONS` ORDER BY `COLLATION_NAME` ASC")