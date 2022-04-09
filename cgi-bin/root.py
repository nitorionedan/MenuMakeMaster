#!/usr/local/bin/python3
# coding: utf-8
# -*- coding: utf-8 -*-

# for debugging
import cgitb
cgitb.enable()
import cgi
import model_test
import view
import controller_test
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import traceback
import sys
import io

# for Japanese
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print('Content-Type: text/html; charset=UTF-8\n')

systemMsg = str()

def addSystemMsg(msg: str):
    global systemMsg
    systemMsg = systemMsg + '>> ' + msg + '<br>'

def main():
    global systemMsg
    form = cgi.FieldStorage()

    ctrl = controller_test.Controller(model_test.ModelSQLite('test0405'), view.View())

    if form.getfirst('/test/create'):
        ctrl.create(form)
    elif form.getfirst('/test/read'):
        ctrl.read()
    elif form.getfirst('/test/update'):
        ctrl.update(form)
    elif form.getfirst('/test/delete'):
        ctrl.delete(form)
    elif form.getfirst('/test/deleteall'):
        ctrl.deleteall()
    elif form.getfirst('/test/generate'):
        ctrl.generate()
    else:
        #404 error
        pass
    
main()