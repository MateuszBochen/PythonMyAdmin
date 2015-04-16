# -*- coding: UTF-8  -*-

import importlib, os

class Kernel:
    
    kernelOS = 0
    config = {}
    autoloader = 0
    imortLib = 0
    responseObject = 0
    
    framework = 0
    templating = 0
    # """ Konstruktor """
    def __init__(self):
        self.kernelOS = os
        self.imortLib = importlib
        
        # Pobieranie ustawien
        configs = importlib.import_module("Config.Config")
        self.config = configs.config
        
       
        # Odpalanie autoloadera
        self.autoloader = importlib.import_module("System.Autoloader.Autoloader")
        self.autoloader = self.autoloader.Autoloader(self);
        
        self.responseObject = self.autoloader.load('System.Http.Response')
       
        
        
        
        requestObject = self.autoloader.load("System.Http.URL", False, True)        
        
        firstSegment = requestObject.getSegment(0);
        
        end = 'Front'
        appName = 'Homepage'
        controller = 'Controller'
        method = 'defaultRun'
        
        segment = 0
        
        
        
        if(firstSegment == self.config['ADMIN_DIR']):
            segment += 1;
            firstSegment = requestObject.getSegment(segment);
            end = 'Back'            
        
        segment += 1;
        
        if(firstSegment != ''):           
            appName = firstSegment
        
        controllerSegment = requestObject.getSegment(segment);
        
        segment += 1;
        
        
        if(controllerSegment != ''):
            controller = controllerSegment
            
        methodSegment = requestObject.getSegment(segment);
        
        if(methodSegment != ''):
            method = methodSegment+'Run'
        # dodatek do szablonów
        self.appName = appName
        self.controller = controller
        # odpalanie managera szablonów
        self.templating = self.autoloader.load('System.Templating.Templating', True, True)
        self.framework = self.autoloader.load("System.Framework.Framework", True, True)
        
        self.beforeApp()
        
        modulePath = 'Applications.'+end+'.'+appName+'.'+controller
        
        if(not(self.autoloader.moduleExists(modulePath))):
            print "nie ma takiego modu³u <b>"+modulePath+"  </b>"
            return False
        
        newApp = importlib.import_module(modulePath)
        
        
            
        controller = getattr(newApp, controller)(self.framework)
        
        if(not(method in dir(controller))):
            print "nie ma takiej metody"
            return False
            
        
            
        controlerres = getattr(controller, method)()        
      
        
        # Wysy³anie nag³ówka do przegl¹darki
        self.responseObject.httpResponse()
        self.templating.display()
        
    def beforeApp(self):
        session = self.autoloader.load('System.Http.Session');
        
        user = session.get('mysqlUser')
        password = session.get('mysqlPassword')    
        host = self.framework.config('MYSQL_HOST')
        port = self.framework.config('MYSQL_PORT')
        
        if(user and password and host and port):
            database = self.framework.module('System.Database.MySql');
            if(not database.connect(host, user, password, port)):
                if(self.appName != 'Authorization'):
                    self.framework.redirect(self.framework.path('Authorization/Login'))
            else:
                baseName = session.get('mysqlDatabase')                 
                if(baseName != ''):
                    session.set('mysqlDatabase', baseName)
                    database.query('USE `'+baseName+'`');
            
        else:
            if(self.appName != 'Authorization'):
                self.framework.redirect(self.framework.path('Authorization/Login'))
                
        