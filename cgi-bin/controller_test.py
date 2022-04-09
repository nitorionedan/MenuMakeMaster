#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from random import randrange
import mvc_exceptions as mvc_exc
import model_test as model
import view as view
import cgi
import cgitb
cgitb.enable()

class Controller(object):
    def __init__(self, model: model.ModelSQLite, view: view.View):
        self.model = model
        self.view = view
        self.item_type = self.model.item_type
    
    def create(self, form: cgi.FieldStorage):
        menu_name = form.getlist('menu_name')[0]
        menu_category = form.getlist('menu_category')[0]
        menu_category_jp = str()

        if menu_category == 'main':
            menu_category_jp = '主菜'
        elif menu_category == 'sub':
            menu_category_jp = '副菜'
        elif menu_category == 'salad':
            menu_category_jp = 'サラダ'

        try:
            self.model.create_item(menu_name, menu_category)
            #body = f'{menu_name}を{menu_category_jp}で登録しました！<br>'
            self.view.create_result(menu_name, menu_category_jp)
            return
        except:
            self.view.already_exist(menu_name, menu_category_jp, '../view/create.html')
            return


    def read(self):
        items = self.model.read_items()

        menu_mains_text = str()
        menu_subs_text = str()
        menu_salads_text = str()

        menu_mains = list(filter(lambda x: x['category'] == 'main', items))
        menu_subs = list(filter(lambda x: x['category'] == 'sub', items))
        menu_salads = list(filter(lambda x: x['category'] == 'salad', items))

        if len(menu_mains) > 0:
            for main in menu_mains:
                menu_mains_text += main['name'] + '<br>'
        else:
            menu_mains_text = 'ありません。<br>'

        if len(menu_subs) > 0:
            for sub in menu_subs:
                menu_subs_text += sub['name'] + '<br>'
        else:
            menu_subs_text = 'ありません。<br>'

        if len(menu_salads) > 0:
            for salad in menu_salads:
                menu_salads_text += salad['name'] + '<br>'
        else:
            menu_salads_text = 'ありません。<br>'
        
        self.view.read(menu_mains_text, menu_subs_text, menu_salads_text)
    
    def update(self, form: cgi.FieldStorage):
        menu_name = form.getlist('menu_name')[0]
        menu_new_category = form.getlist('menu_category')[0]

        try:
            menu_old_category = self.model.read_item(menu_name)['category']
        except:
            self.view.not_stored(menu_name, '../view/update.html')
            return

        body = str()
        menu_new_category_jp = str()
        menu_old_category_jp = str()

        if menu_new_category == 'main':
            menu_new_category_jp = '主菜'
        elif menu_new_category == 'sub':
            menu_new_category_jp = '副菜'
        elif menu_new_category == 'salad':
            menu_new_category_jp = 'サラダ'

        if menu_old_category == 'main':
            menu_old_category_jp = '主菜'
        elif menu_old_category == 'sub':
            menu_old_category_jp = '副菜'
        elif menu_old_category == 'salad':
            menu_old_category_jp = 'サラダ'

        self.model.update_item(menu_name, menu_new_category)
        body = f'{menu_name}のカテゴリを{menu_old_category_jp}から{menu_new_category_jp}へ更新しました！<br>'
        
        print(body)
        print('<a href="../index.html">Back</a>')

    def delete(self, form: cgi.FieldStorage):
        body = str()

        try:
            menu_name = form.getlist('menu_name')[0]
            self.model.delete_item(menu_name)
            body = f'{menu_name}を削除しました。<br>'
        except:
            body += 'その料理は存在してないです。<br>'

        #self.view.delete(menu_name, old_item['category'])


        print(body)
        print('<a href="../delete.html">Back</a>')
    
    def deleteall(self):
        old_items = self.model.read_items()
        body = str()

        if len(old_items) > 0:
            for item in old_items:
                self.model.delete_item(item['name'])
                body += '・' + item['name'] + '<br>'
            #self.view.deleteall(old_items)

            body += 'を削除しました。<br>'
        else:
            body += '登録料理はありません。<br>'

        print(body)
        print('<a href="../view/delete.html">Back</a>')

    def generate(self):
        menu_main_result = str()
        menu_sub_result = str()
        menu_salad_result = str()
        items = self.model.read_items()

        # read all menus
        menu_mains = list(filter(lambda x: x['category'] == 'main', items))
        menu_subs = list(filter(lambda x: x['category'] == 'sub', items))
        menu_salads = list(filter(lambda x: x['category'] == 'salad', items))

        if len(menu_mains) < 1:
            menu_main_result = '水'
        else:
            menu_main_result = menu_mains[randrange(len(menu_mains))]['name']

        if len(menu_subs) < 1:
            menu_sub_result = '水'
        else:
            menu_sub_result = menu_subs[randrange(len(menu_subs))]['name']

        if len(menu_salads) < 1:
            menu_salad_result = '水'
        else:
            menu_salad_result = menu_salads[randrange(len(menu_salads))]['name']

        self.view.generate(menu_main_result, menu_sub_result, menu_salad_result)

    def update_item_type(self, new_item_type):
        old_item_type = self.model.item_type
        self.model.item_type = new_item_type
        # self.view.display_change_item_type(old_item_type, new_item_type)
