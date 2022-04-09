#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import mvc_exceptions as mvc_exc

class SQLiteBackend:

    def __init__(self, DB_name):
        self.__DB_name = DB_name

    def connect_to_db(self):
        """Connect to a sqlite DB. Create the database if there isn't one yet.

        Open a connection to a SQLite DB (either a DB file or an in-memory DB).
        When a database is accessed by multiple connections, and one of the
        processes modifies the database, the SQLite database is locked until that
        transaction is committed.

        Parameters
        ----------
        db : str
            database name (without .db extension). If None, create an In-Memory DB.

        Returns
        -------
        connection : sqlite3.Connection
            connection object
        """
        if self.__DB_name is None:
            mydb = ':memory:'
            # print('New connection to in-memory SQLite DB...')
        else:
            mydb = '{}.db'.format(self.__DB_name)
            # print('New connection to SQLite DB')
        connection = sqlite3.connect(mydb)
        return connection


    # TODO: use this decorator to wrap commit/rollback in a try/except block ?
    # see http://www.kylev.com/2009/05/22/python-decorators-and-database-idioms/
    def connect(func):
        """Decorator to (re)open a sqlite database connection when needed.

        A database connection must be open when we want to perform a database query
        but we are in one of the following situations:
        1) there is no connection
        2) the connection is closed

        Parameters
        ----------
        func : function
            function which performs the database query

        Returns
        -------
        inner func : function
        """
        def inner_func(self, conn, *args, **kwargs):
            try:
                # I don't know if this is the simplest and fastest query to try
                conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')  
            except (AttributeError, ProgrammingError):
                conn = self.connect_to_db(self.__DB_name)
            return func(self, conn, *args, **kwargs)
        return inner_func

    def disconnect_from_db(self, db=None, conn=None):
        if db is not self.__DB_name:
            print("You are trying to disconnect from a wrong DB")
        if conn is not None:
            conn.close()

    @connect
    def create_table(self, conn, table_name):
        table_name = self.scrub(table_name)
        sql = 'CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
                'name TEXT UNIQUE, category TEXT)'.format(table_name)
        try:
            conn.execute(sql)
        except OperationalError as e:
            #print('in create_table: ' + str(e))
            pass

    def scrub(self, input_string):
        """Clean an input string (to prevent SQL injection).

        Parameters
        ----------
        input_string : str

        Returns
        -------
        str
        """
        return ''.join(k for k in input_string if k.isalnum())

    @connect
    def insert_one(self, conn, name, category, table_name):
        table_name = self.scrub(table_name)
        sql = "INSERT INTO {} ('name', 'category') VALUES (?, ?)".format(table_name)
        try:
            conn.execute(sql, (name, category))
            conn.commit()
        except IntegrityError as e:
            raise mvc_exc.ItemAlreadyStored('{}: "{}" already stored in table "{}"'.format(e, name, table_name))

    @connect
    def insert_many(self, conn, items, table_name):
        table_name = self.scrub(table_name)
        sql = "INSERT INTO {} ('name', 'category') VALUES(?, ?)".format(table_name)
        entries = list()
        for x in items:
            entries.append((x['name'], x['category']))
        try:
            conn.executemany(sql, entries)
            conn.commit()
        except IntegrityError as e:
            return '{}: at least one in {} was already stored in table "{}"'.format(e, [x['name'] for x in items], table_name)

    def tuple_to_dict(self, mytuple):
        mydict = dict()
        mydict['id'] = mytuple[0]
        mydict['name'] = mytuple[1]
        mydict['category'] = mytuple[2]
        return mydict

    @connect
    def select_one(self, conn, item_name, table_name):
        table_name = self.scrub(table_name)
        item_name = self.scrub(item_name)
        sql = 'SELECT * FROM {} WHERE name="{}"'.format(table_name, item_name)
        c = conn.execute(sql)
        result = c.fetchone()
        if result is not None:
            return self.tuple_to_dict(result)
        else:
            raise mvc_exc.ItemNotStored(
                'Cannot read {} because it is not stored in table {}'.format(item_name, table_name))

    @connect
    def select_all(self, conn, table_name):
        table_name = self.scrub(table_name)
        sql = 'SELECT * FROM {}'.format(table_name)
        c = conn.execute(sql)
        results = c.fetchall()
        return list(map(lambda x: self.tuple_to_dict(x), results))

    @connect
    def update_one(self, conn, name, category, table_name):
        table_name = self.scrub(table_name)
        sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1)'.format(table_name)
        c = conn.execute(sql_check, (name,)) # we need the comma
        result = c.fetchone()
        if result[0]:
            sql_update = 'UPDATE {} SET category=? WHERE name=?'.format(table_name)
            c.execute(sql_update, (category, name))
            conn.commit()
        else:
            raise mvc_exc.ItemNotStored('Can\'t update "{}" because it\'s not stored in table "{}"'.format(name, table_name))

    @connect
    def delete_one(self, conn, name, table_name):
        table_name = self.scrub(table_name)
        sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE name=? LIMIT 1)'.format(table_name)
        table_name = self.scrub(table_name)
        sql_delete = 'DELETE FROM {} WHERE name=?'.format(table_name)
        c = conn.execute(sql_check, (name,))
        result = c.fetchone()
        if result[0]:
            c.execute(sql_delete, (name,))
            conn.commit()
        else:
            raise mvc_exc.ItemNotStored('Can\'t delete "{}" because it\'s not stored in table "{}"'.format(name, table_name))
