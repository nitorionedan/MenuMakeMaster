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
import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import sqlite_backend
import traceback

systemMsg = '>> no message<br>'

def render(controller: controller_test.Controller):
    global systemMsg
    renderingText = """
    <html>

        <head>
            <meta charset="utf-8">
            <title>Exponents Calculator</title>
        </head>

        <body>
            <h1>Rui chan Uchu Ichi Daisuki!!!</h1>
            //////////////////////////////////////<br>
            sqlite3 version is {}.<br>
            system message:<br>
            {}
            //////////////////////////////////////<br>
            <br>
            {}<br>
            <br>
            <br>
            <a href="../index.html">Back</a>
        </body>

    </html>
    """.format(sqlite3.version, systemMsg, str(controller.show_item('unko')))

    print(renderingText)

def addSystemMsg(msg: str):
    global systemMsg
    systemMsg = '>> ' + systemMsg + msg + '<br>'

def main():
    global systemMsg

    try:
        controller = controller_test.Controller(model_test.ModelSQLite(), view.View())
        controller.insert_item('unko', 'main')
    except:
        addSystemMsg(traceback.format_exc())

    render(controller)


main()