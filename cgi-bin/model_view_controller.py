#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sqlite_backend
import mvc_exceptions as mvc_exc

class View(object):
    @staticmethod
    def show_bullet_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))
    
    @staticmethod
    def show_number_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

    @staticmethod
    def show_item(item_type, item, item_info):
        print('//////////////////////////////////////////////////////////////')
        print('Good news, we have some {}!'.format(item.upper()))
        print('{} INFO: {}'.format(item_type.upper(), item_info))
        print('//////////////////////////////////////////////////////////////')

    @staticmethod
    def display_missing_item_error(item, err):
        print('**************************************************************')
        print('We are sorry, we have no {}!'.format(item.upper()))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_already_stored_error(item, item_type, err):
        print('**************************************************************')
        print('Hey! We already have {} in our {} list!'.format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_not_yet_stored_error(item, item_type, err):
        print('**************************************************************')
        print('We don\'t have any {} in our {} list. Please insert it first!'.format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('**************************************************************')

    @staticmethod
    def display_item_stored(item, item_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Hooray! We have just added some {} to our {} list!'.format(item.upper(), item_type))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    @staticmethod
    def display_change_item_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change item type from "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change {} price: {} --> {}'.format(item, o_price, n_price))
        print('Change {} quantity: {} --> {}'.format(item, o_quantity, n_quantity))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_deletion(name):
        print('--------------------------------------------------------------')
        print('We have just removed {} from our list'.format(name))
        print('--------------------------------------------------------------')

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        items = self.model.read_items()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)
        return items

    def show_item(self, item_name):
        try:
            item = self.model.read_item(item_name)
            item_type = self.model.item_type
            self.view.show_item(item_type, item_name, item)
        except mvc_exc.ItemAlreadyStored as e:
            self.view.display_missing_item_error(item_name, e)

    def show_item(self, item_name):
        try:
           item = self.model.read_item(item_name)
           item_type = self.model.item_type
           self.view.show_item(item_type, item_type, item)
        except mvc_exc.ItemNotStored as e:
            self.view.display_missing_item_error(item_name, e)

    def insert_item(self, name, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than 0 or equal to 0'
        item_type = self.model.item_type
        try:
            self.model.create_item(name, price, quantity)
            self.view.display_item_stored(name, item_type)
        except mvc_exc.ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(name, item_type, e)
    
    def update_item(self, name, price, quantity):
        assert price > 0, 'price must be greater than 0'
        assert quantity >= 0, 'quantity must be greater than 0 or equal to 0'
        item_type = self.model.item_type

        try:
            older = self.model.read_item(name)
            self.model.update_item(name, price, quantity)
            self.view.display_item_updated(name, older['price'], older['quantity'], price, quantity)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(name, item_type, e)
            # if the item is not yet stored and we performed an update, we have
            # 2 options: do nothing or call insert_item to add it.
            # self.insert_item(name, price, quantity)

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        self.view.display_change_item_type(old_item_type, new_item_type)

    def delete_item(self, name):
        item_type = self.model.item_type
        try:
            self.model.delete_item(name)
            self.view.display_item_deletion(name)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(name, item_type, e)
    
    def delete_allitems(self):
        item_type = self.model.item_type
        delete_items = self.model.read_items()

        try:
            for item in delete_items:
                self.model.delete_item(item['name'])
                self.view.display_item_deletion(item['name'])
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error('items', item_type, e)    

class ModelSQLite(object):
    def __init__(self, DB_name=None, application_items=None):
        self._item_type = 'product'
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

    def create_item(self, name, price, quantity):
        self.__sqlite_backend.insert_one(self.connection, name, price, quantity, self.item_type)

    def create_items(self, items):
        self.__sqlite_backend.insert_many(self.connection, items, self.item_type)

    def read_item(self, name):
        return self.__sqlite_backend.select_one(
            self.connection, name, table_name=self.item_type)

    def read_items(self):
        return self.__sqlite_backend.select_all(
            self.connection, table_name=self.item_type)

    def update_item(self, name, price, quantity):
        self.__sqlite_backend.update_one(
            self.connection, name, price, quantity, table_name=self.item_type)

    def delete_item(self, name):
        self.__sqlite_backend.delete_one(
            self.connection, name, table_name=self.item_type)

# if __name__ == '__main__':
#     controller = Controller(ModelSQLite(DB_name='myDB'), View())
#     controller.show_items()
#     controller.delete_allitems()
