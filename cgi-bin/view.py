#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

class View(object):
    @staticmethod
    def create(menu_main, menu_sub, menu_salad):
        # load html file
        with open(r'../view/create.html', 'r', encoding="utf-8") as file:
            html = file.read()
        file.close

        page_data = {}
        page_data['menu_main'] = menu_main
        page_data['menu_sub'] = menu_sub
        page_data['menu_salad'] = menu_salad

        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)

    @staticmethod
    def read(menu_mains: str, menu_subs: str, menu_salads: str):
        # load html file
        with open(r'../view/read.html', 'r', encoding="utf-8") as file:
            html = file.read()
        file.close

        page_data = {}
        page_data['menu_mains'] = menu_mains
        page_data['menu_subs'] = menu_subs
        page_data['menu_salads'] = menu_salads

        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)

    @staticmethod
    def delete(item_name):
        pass

    @staticmethod
    def deleteall(items):
        pass

    @staticmethod
    def already_exist(menu_name: str, menu_category: str, link_to_back: str):
        with open(r'../view/alreadyexist.html', 'r', encoding="utf-8") as file:
             html = file.read()
        file.close

        page_data = {}
        page_data['menu_name'] = menu_name
        page_data['menu_category'] = menu_category
        page_data['link_to_back'] = link_to_back
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)

    @staticmethod
    def not_stored(menu_name: str, link_to_back: str):
        with open(r'../view/notstored.html', 'r', encoding="utf-8") as file:
             html = file.read()
        file.close

        page_data = {}
        page_data['menu_name'] = menu_name
        page_data['link_to_back'] = link_to_back
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)

    @staticmethod
    def create_result(menu_name: str, menu_category: str):
        with open(r'../view/create_result.html', 'r', encoding="utf-8") as file:
             html = file.read()
        file.close

        page_data = {}
        page_data['menu_name'] = menu_name
        page_data['menu_category'] = menu_category
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)

    @staticmethod
    def generate(menu_main: str, menu_sub: str, menu_salad: str):
        with open(r'../view/generate.html', 'r', encoding="utf-8") as file:
             html = file.read()
        file.close

        page_data = {}
        page_data['menu_main'] = menu_main
        page_data['menu_sub'] = menu_sub
        page_data['menu_salad'] = menu_salad
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        print(html)
       


    # @staticmethod
    # def display_missing_item_error(item, err):
    #     print('**************************************************************')
    #     print('We are sorry, we have no {}!'.format(item.upper()))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')

    # @staticmethod
    # def display_item_already_stored_error(item, item_type, err):
    #     print('**************************************************************')
    #     print('Hey! We already have {} in our {} list!'.format(item.upper(), item_type))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')

    # @staticmethod
    # def display_item_not_yet_stored_error(item, item_type, err):
    #     print('**************************************************************')
    #     print('We don\'t have any {} in our {} list. Please insert it first!'.format(item.upper(), item_type))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')

    # @staticmethod
    # def display_item_stored(item, item_type):
    #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #     print('Hooray! We have just added some {} to our {} list!'.format(item.upper(), item_type))
    #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    # @staticmethod
    # def display_change_item_type(older, newer):
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #     print('Change item type from "{}" to "{}"'.format(older, newer))
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    # @staticmethod
    # def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #     print('Change {} price: {} --> {}'.format(item, o_price, n_price))
    #     print('Change {} quantity: {} --> {}'.format(item, o_quantity, n_quantity))
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
