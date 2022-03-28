#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sqlite_backend
import mvc_exceptions as mvc_exc

class ModelSQLite(object):
    def __init__(self, DB_name=None, application_items=None):
        self._item_type = 'menu'
        self.__sqlite_backend = sqlite_backend.SQLiteBackend(DB_name)
        self._connection = self.__sqlite_backend.connect_to_db()
        self.__sqlite_backend.create_table(self.connection, self._item_type)
        if application_items is not None:
            self.create_items(application_items)

    @property
    def connection(self):
        return self._connection

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, name, category):
        self.__sqlite_backend.insert_one(self.connection, name, category, self.item_type)

    def create_items(self, items):
        self.__sqlite_backend.insert_many(self.connection, items, self.item_type)

    def read_item(self, name):
        return self.__sqlite_backend.select_one(
            self.connection, name, table_name=self.item_type)

    def read_items(self):
        return self.__sqlite_backend.select_all(
            self.connection, table_name=self.item_type)

    def update_item(self, name, category):
        self.__sqlite_backend.update_one(
            self.connection, name, category, table_name=self.item_type)

    def delete_item(self, name):
        self.__sqlite_backend.delete_one(
            self.connection, name, table_name=self.item_type)
