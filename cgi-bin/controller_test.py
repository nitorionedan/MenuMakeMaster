#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import mvc_exceptions as mvc_exc
import model_test as model
import view as view

class Controller(object):
    def __init__(self, model: model.ModelSQLite, view: view.View):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        items = self.model.read_items()
        item_type = self.model.item_type
        # if bullet_points:
        #     self.view.show_bullet_point_list(item_type, items)
        # else:
        #     self.view.show_number_point_list(item_type, items)
        return items

    def show_item(self, item_name):
        item = self.model.read_item(item_name)
        
        # try:
        #     item_type = self.model.item_type
        #     self.view.show_item(item_type, item_name, item)
        # except mvc_exc.ItemAlreadyStored as e:
        #     self.view.display_missing_item_error(item_name, e)
        
        return item

    def insert_item(self, name, category):
        # assert price > 0, 'price must be greater than 0'

        item_type = self.model.item_type
        try:
            self.model.create_item(name, category)
            # self.view.display_item_stored(name, item_type)
        except mvc_exc.ItemAlreadyStored as e:
            # self.view.display_item_already_stored_error(name, item_type, e)
            return e

    def update_item(self, name, category):
        item_type = self.model.item_type

        try:
            older = self.model.read_item(name)
            self.model.update_item(name, category)
            # self.view.display_item_updated(name, older['name'], older['category'])
        except mvc_exc.ItemNotStored as e:
            # self.view.display_item_not_yet_stored_error(name, item_type, e)
            # if the item is not yet stored and we performed an update, we have
            # 2 options: do nothing or call insert_item to add it.
            # self.insert_item(name, price, quantity)
            return e

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        # self.view.display_change_item_type(old_item_type, new_item_type)

    def delete_item(self, name):
        item_type = self.model.item_type
        try:
            self.model.delete_item(name)
            # self.view.display_item_deletion(name)
        except mvc_exc.ItemNotStored as e:
            # self.view.display_item_not_yet_stored_error(name, item_type, e)
            return e
    
    def delete_allitems(self):
        item_type = self.model.item_type
        delete_items = self.model.read_items()

        try:
            for item in delete_items:
                self.model.delete_item(item['name'])
                # self.view.display_item_deletion(item['name'])
        except mvc_exc.ItemNotStored as e:
            # self.view.display_item_not_yet_stored_error('items', item_type, e)
            return e