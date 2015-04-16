# -*- coding: UTF-8  -*-

import re


class TableManager:
    
    framework = 0
    
    functionsWithoutParam = ['CURRENT_DATE', 'CURRENT_DATE', 'CURRENT_TIME',
                            'CURRENT_TIMESTAMP', 'CURTIME', 'LOCALTIME', 'LOCALTIMESTAMP',
                            'SYSDATE', 'UNIX_TIMESTAMP', 'UTC_DATE', 'UTC_TIME', 'UTC_TIMESTAMP', 'UUID', 'CONNECTION_ID'
                            'CURRENT_USER', 'DATABASE', 'FOUND_ROWS', 'LAST_INSERT_ID', 'ROW_COUNT','SCHEMA','NOW', 'MOD','PI', 'RAND'
                            'SESSION_USER', 'SYSTEM_USER', 'USER', 'VERSION'
                            ]
    
    def __init__(self, framework):        
        self.framework = framework
    
    def createRun(self):
        
        mysql = self.framework.module('System.Database.MySql')
        
        engines = mysql.getEngines()
        collations = mysql.getCollations()
        
        tableStruct = self.framework.module('System.Http.Session').get('tableStruct')
        self.framework.module('System.Http.Session').set('tableStruct', {})
        
        if(not type(tableStruct).__name__ == 'dict'):
            tableStruct = ''
        
        
        return self.framework.render('create', {'engines': engines, 'collations': collations, 'tableStruct': tableStruct})
        
        
    def saveTableRun(self):
        database = self.framework.module('System.Database.MySql')
        form = self.framework.module('System.Http.Header.Post')
        
       
        
        controlInput = form.get('controlInput')        
        
        
        tableName = form.get('tableName')
        storageEngine = form.get('storageEngine')
        tableCollations = form.get('tableCollations') 
        tableComment = form.get('tableComment') # optional
        partitionDefinition = form.get('partitionDefinition') # optional
        
        collations = []
        if(tableCollations):
            collations = tableCollations.split(';')
        
        mysqlQuery = "CREATE TABLE `"+tableName+'` ('+"\n"
        
        allColumns = len(controlInput)-1
        
        idexes = {'INDEX': [], 'UNIQUE': [], 'FULLTEXT': []}
        
        for index, value in enumerate(controlInput):            
            mysqlQuery += '`'+form.getListByIndex('columnName', index)+'`'
            mysqlQuery += ' '+self.getDataType(form.getListByIndex('columnType', index), form.getListByIndex('columnLength', index), form.getListByIndex('columnAttribute', index), form.getListByIndex('columnCollations', index), form.getListByIndex('columnValues', index))
            mysqlQuery += (' NULL' if(form.getListByIndex('columnIsNULL', index) == 1) else ' NOT NULL')
            mysqlQuery += (' DEFAULT \''+form.getListByIndex('columnDefaultType', index) if(form.getListByIndex('columnDefaultType', index)) else '')
            mysqlQuery += (" AUTO_INCREMENT" if(form.getListByIndex('columnAutoIncrement', index) == '1') else "")
            mysqlQuery += (" PRIMARY KEY" if(form.getListByIndex('columnIndex', index) == 'PRIMARY') else "")            
            mysqlQuery += (" COMMENT '"+form.getListByIndex('columnComment', index)+"'" if(form.getListByIndex('columnComment', index)) else "")            
            mysqlQuery += (", \n" if(allColumns > index) else "")
            
            if(form.getListByIndex('columnIndex', index) in ('INDEX', 'UNIQUE', 'FULLTEXT')):
                indexName = form.getListByIndex('columnIndex', index)
                idexes[indexName].append('`'+form.getListByIndex('columnName', index)+'`')
        
        for indexKey in idexes:
            if(len(idexes[indexKey]) > 0):
                mysqlQuery +=", \n"+indexKey+"("
                mysqlQuery += ', '.join(idexes[indexKey])
                mysqlQuery += ')'
                
        mysqlQuery += "\n"+') ENGINE='+storageEngine+''+(' CHARACTER SET '+collations[1]+" COLLATE "+collations[0] if(tableCollations) else '')
        mysqlQuery += (" COMMENT='"+tableComment+"'" if(tableComment) else "")
        
               
        if(database.query(mysqlQuery)):        
            self.framework.module('System.Http.Session').setNotice('success', 'Table was created')
            
        else:           
            keepDataForNextTry = {
            'table': {
                'tableName': tableName,
                'storageEngine': storageEngine,
                'tableCollations': tableCollations,
                'tableComment': tableComment,
                'partitionDefinition': partitionDefinition
                },
            'columns':{
                'columnName': form.get('columnName', True),
                'controlInput': form.get('controlInput', True),
                'columnType': form.get('columnType', True),
                'columnLength': form.get('columnLength', True),
                'columnDefaultType': form.get('columnDefaultType', True),
                'columnCollations': form.get('columnCollations', True),
                'columnAttribute': form.get('columnAttribute', True),
                'columnIsNULL': form.get('columnIsNULL', True),
                'columnIndex': form.get('columnIndex', True),
                'columnAutoIncrement': form.get('columnAutoIncrement', True),
                'columnComment': form.get('columnComment', True),
                }
            }            
            self.framework.module('System.Http.Session').set('tableStruct', keepDataForNextTry)
            
        self.framework.module('System.Http.Session').setNotice('secondary', database.getLastQuery())
        return self.framework.module('System.Http.Response').redirectToLastUrl()
      

    '''
    * generate column type definition
    '''
    def getDataType(self, type, length, atributes, collation, values):
        expCollations = []
        if(collation):
            expCollations = collation.split(';')
        
        # CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL 
        
        ret = ''
        
        if type in ('BIT', 'BINARY', 'VARBINARY'):           
            ret = type+'('+('11' if(length == '') else length)+')'
            
        elif type in ('TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT', 'REAL', 'DOUBLE', 'FLOAT', 'DECIMAL', 'NUMERIC'):
            ret = type+'('+('11' if(length == '') else length)+') '+atributes
        
        elif type in ('CHAR', 'VARCHAR'):
            ret = type+'('+length+')'+(' CHARACTER SET '+expCollations[1]+' COLLATE '+ expCollations[0] if(collation) else '')
            
        elif type in ('TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT'):
            ret = type+' '+('BINARY' if(atributes == 'BINARY') else '')+(' CHARACTER SET '+expCollations[1]+' COLLATE '+ expCollations[0] if(collation) else '')
         
        elif type in ('ENUM', 'SET'):
            ret = type+'('+values+')'+(' CHARACTER SET '+expCollations[1]+' COLLATE '+ expCollations[0] if(collation) else '')
            
        else:
            ret = type
                
            
        return ret
     
     
    '''
    * remove table
    '''
    def dropRun(self):
        tableForDrop = self.framework.module('System.Http.URL').getSegment(3);
        
        mysql = self.framework.module('System.Database.MySql')
        
        mysql.query("DROP TABLE `"+tableForDrop+"`");
        
        
        
        self.framework.module('System.Http.Session').setNotice('success', 'Table was dropped')
        self.framework.module('System.Http.Session').setNotice('secondary', mysql.getLastQuery())
        
        return self.framework.module('System.Http.Response').redirectToLastUrl()
    
    ''' 
    * removing all records, but save table 
    '''
    def truncateRun(self):
        tableForDrop = self.framework.module('System.Http.URL').getSegment(3);
        
        mysql = self.framework.module('System.Database.MySql')
        
        mysql.query("TRUNCATE TABLE `"+tableForDrop+"`");
        
        
        
        self.framework.module('System.Http.Session').setNotice('success', 'Table was dropped')
        self.framework.module('System.Http.Session').setNotice('secondary', mysql.getLastQuery())
        
        return self.framework.module('System.Http.Response').redirectToLastUrl()
        
    def insertRun(self):
        table = self.framework.module('System.Http.URL').getSegment(3);
        columns = self.framework.module('System.Database.MySql').query("SHOW COLUMNS FROM "+table)
        
        postValues = self.framework.module('System.Http.Session').get('valuesStruct')
        self.framework.module('System.Http.Session').set('valuesStruct', {})
        
        return self.framework.render('insert', {'columns': columns, 'table': table, 'postValues': postValues}) 
    
    '''
    * saving record
    '''
    def saveRun(self):
        table = self.framework.module('System.Http.URL').getSegment(3);
        
        form = self.framework.module('System.Http.Header.Post')
        
        mysql = self.framework.module('System.Database.MySql')
        
        columns = mysql.query("SHOW COLUMNS FROM "+table)
        
        onlyColumnNames = []
        onlyValues = []
        
        for (index, column) in enumerate(columns):
            onlyColumnNames.append('`'+column[0]+'`')
            
            function = form.getListByIndex('functions', index)
            value = form.getListByIndex('values', index)
            valueToInsert = '\'\''
            if(function != '' and (function in self.functionsWithoutParam)):
                valueToInsert = function+'()'
            elif(function != '' and value != ''):
                valueToInsert = function+'(\''+value+'\')'
            elif(value != ''):
                valueToInsert = "'"+value+"'"
                
            onlyValues.append(str(valueToInsert))

             
        onlyColumnNames = ', '.join(onlyColumnNames)
        onlyValues = ', '.join(onlyValues)
        
       
        
        
        if(mysql.query("INSERT INTO `"+table+"` ("+onlyColumnNames+") VALUES ("+onlyValues+")") != False):
            self.framework.module('System.Http.Session').setNotice('success', 'Record was added')
        else:
            self.framework.module('System.Http.Session').setNotice('alert', 'Record was not added')
            keepDataForNextTry = {
                'functions': form.get('functions', True),
                'text': form.get('values', True)
            }            
            self.framework.module('System.Http.Session').set('valuesStruct', keepDataForNextTry)
        
        self.framework.module('System.Http.Session').setNotice('secondary', mysql.getLastQuery())
        return self.framework.module('System.Http.Response').redirectToLastUrl()
        
       
       
    def dropColumnRun(self):
        url = self.framework.module('System.Http.URL')
        table = url.getSegment(3)
        column = url.getSegment(4)
        
        mysql = self.framework.module('System.Database.MySql')
        mysql.query('ALTER TABLE `'+table+'` DROP `'+column+'`')
        
        self.framework.module('System.Http.Session').setNotice('success', 'Column was dropped')
        self.framework.module('System.Http.Session').setNotice('secondary', mysql.getLastQuery())
        return self.framework.module('System.Http.Response').redirectToLastUrl()        
       
    def createNewColumnRun(self):
        url = self.framework.module('System.Http.URL')
        table = url.getSegment(3)
        direction = url.getSegment(4)
        column = url.getSegment(5)
        
        tableStruct = self.framework.module('System.Http.Session').get('tableStruct')
        self.framework.module('System.Http.Session').set('tableStruct', {})
        
        
        
        return self.framework.render('createNewColumn', {'collations': self.framework.module('System.Database.MySql').getCollations(), 'table': table, 'direction': direction, 'column': column, 'tableStruct': tableStruct})
        
    def saveNewColumnsRun(self):    
        url = self.framework.module('System.Http.URL')
        table = url.getSegment(3)
        direction = url.getSegment(4)
        column = url.getSegment(5)
        
        mysql = self.framework.module('System.Database.MySql')
        form = self.framework.module('System.Http.Header.Post')
        
        #print "Content-type: text/html;  charset: UTF-8; \n\n"
        
        controlInput = form.get('controlInput')
        
        idexes = {'INDEX': [], 'UNIQUE': [], 'FULLTEXT': []}
        
        mysqlQuery = 'ALTER TABLE `'+table+'` ADD ';
        
        allColumns = len(controlInput)-1
        lastAdded = column
        for index, value in enumerate(controlInput):     
            currentColumn = form.getListByIndex('columnName', index)
            mysqlQuery += '`'+currentColumn+'`'
            mysqlQuery += ' '+self.getDataType(form.getListByIndex('columnType', index), form.getListByIndex('columnLength', index), form.getListByIndex('columnAttribute', index), form.getListByIndex('columnCollations', index), form.getListByIndex('columnValues', index))
            mysqlQuery += (' NULL' if(form.getListByIndex('columnIsNULL', index) == 1) else ' NOT NULL')
            mysqlQuery += (' DEFAULT \''+form.getListByIndex('columnDefaultType', index) if(form.getListByIndex('columnDefaultType', index)) else '')
            mysqlQuery += (" AUTO_INCREMENT" if(form.getListByIndex('columnAutoIncrement', index) == '1') else "")
            mysqlQuery += (" PRIMARY KEY" if(form.getListByIndex('columnIndex', index) == 'PRIMARY') else "")            
            mysqlQuery += (" COMMENT '"+form.getListByIndex('columnComment', index)+"'" if(form.getListByIndex('columnComment', index)) else "")            
            mysqlQuery += (" AFTER `"+lastAdded+"`" if(direction == 'after') else "")
            mysqlQuery += (" FIRST" if(direction == 'first') else "")
            mysqlQuery += (", ADD \n" if(allColumns > index) else "")
            
            if(direction == 'first'):
                direction = 'after'
            
            lastAdded = currentColumn
            
            if(form.getListByIndex('columnIndex', index) in ('INDEX', 'UNIQUE', 'FULLTEXT')):
                indexName = form.getListByIndex('columnIndex', index)
                idexes[indexName].append('`'+form.getListByIndex('columnName', index)+'`')
                
        for indexKey in idexes:
            if(len(idexes[indexKey]) > 0):
                mysqlQuery +=", ADD \n"+indexKey+"("
                mysqlQuery += ', '.join(idexes[indexKey])
                mysqlQuery += ')'
        
        if(mysql.query(mysqlQuery) != False):
            self.framework.module('System.Http.Session').setNotice('success', 'Columns was added to the table')
        else:
            self.framework.module('System.Http.Session').setNotice('alert', 'Unable to add columns to the table')
            
            keepDataForNextTry = {            
            'columns':{
                'columnName': form.get('columnName', True),
                'controlInput': form.get('controlInput', True),
                'columnType': form.get('columnType', True),
                'columnLength': form.get('columnLength', True),
                'columnDefaultType': form.get('columnDefaultType', True),
                'columnCollations': form.get('columnCollations', True),
                'columnAttribute': form.get('columnAttribute', True),
                'columnIsNULL': form.get('columnIsNULL', True),
                'columnIndex': form.get('columnIndex', True),
                'columnAutoIncrement': form.get('columnAutoIncrement', True),
                'columnComment': form.get('columnComment', True),
                }
            }            
            self.framework.module('System.Http.Session').set('tableStruct', keepDataForNextTry)
            
        
        self.framework.module('System.Http.Session').setNotice('secondary', mysql.getLastQuery())
        return self.framework.module('System.Http.Response').redirectToLastUrl()
        
    def changeColumnsRun(self):
        tableStruct = {}
        table = self.framework.module('System.Http.URL').getSegment(3)
        mysql = self.framework.module('System.Database.MySql')
        form = self.framework.module('System.Http.Header.Post')
        columnsToChange = form.get('columnToChange', True)
        
        columnsToChange = str(columnsToChange).replace('[', '').replace(']', '')
        
        if(columnsToChange == ''):
            self.framework.module('System.Http.Session').setNotice('alert', 'There you have no columns for to change')
            self.framework.redirect(self.framework.path('Tables/Show/struct/'+table))
        
        columns = mysql.query("SELECT * FROM `information_schema`.`COLUMNS` WHERE `TABLE_NAME` = '"+table+"' AND `COLUMN_NAME` IN ("+str(columnsToChange)+")")
        
        #self.framework.print_r(columns)
        #print "`COLUMN_NAME` IN ("+columnsToChange+")"
        #print columnsToChange
        
        collations = mysql.getCollations()
        
        columnsNames = []
        controlInputs = []
        columnTypes = []
        columnLengths = []
        columnDefaultTypes = []
        columnCollations = []
        columnAttributes = []
        columnIsNULLs = []
        columnIndexs = []
        columnAutoIncrements = []
        columnComments = []
        
        pattern = re.compile(r'\((.*?)\)')
        pattern2 = re.compile(r'^(.*?)(\(([0-9]+)\))*$')
        
        for column in columns:
            
            columnsNames.append(column[3])
            controlInputs.append(column[3])
            columnTypes.append(column[7].upper())
                            
            m = re.match(pattern2, column[14])
            #columnLengths.append((m.group(3) if(m.group(3)) else column[14]))
            columnLengths.append((m.group(3) if(m.group(3)) else ''))
            columnDefaultTypes.append(column[5])
            columnCollations.append(str(column[13])+';'+str(column[12]))
            columnAttributes.append('')
            columnIsNULLs.append(column[6])
            columnIndexs.append(column[15])
            columnAutoIncrements.append(column[16])
            columnComments.append(column[18])
            
               # columnDefaultTypes.append()
                
        #self.framework.print_r(columnCollations)
        
        tableStruct = {            
            'columns':{
                'columnName': columnsNames,
                'controlInput': controlInputs,
                'columnType': columnTypes,
                'columnLength': columnLengths,
                'columnDefaultType': columnDefaultTypes,
                'columnCollations': columnCollations,
                'columnAttribute': columnAttributes,
                'columnIsNULL': columnIsNULLs,
                'columnIndex': columnIndexs,
                'columnAutoIncrement': columnAutoIncrements,
                'columnComment': columnComments,
                }
            } 
        
        return self.framework.render('changeColumns', {'collations': collations, 'tableStruct': tableStruct})
        
        
    def updateColumnsRun(self):
        