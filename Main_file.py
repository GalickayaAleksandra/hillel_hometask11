from Read_files import read_file_pickle
from Read_files import write_file_pickle
from Constants import NAME_FILE_DB_GOODS
from Constants import PARAMETRS_FOR_DICT_GOODS
from Constants import NAME_DOCUMENTS
from Constants import MARKUP
from Regular_pattern import pattern_dates
from Regular_pattern import pattern_float_numbers
import datetime


class AccountingForGoodsStore:
    def __init__(self, name_document, name_goods, amount, price='0.00', new_date=None, nm_doc=None):
        self.name_document = name_document
        self.name_goods = name_goods
        self.amount = amount
        self.price = price
        self.rest_partion = amount
        self.new_date = new_date
        self.number_document = nm_doc

    def __work_method_get_data_from_db(self):
        num_document = self.number_document
        num_document += 1
        values = [self.name_document, self.name_goods, self.amount, self.price,
                  self.rest_partion, self.new_date, num_document]
        filds = dict(zip(PARAMETRS_FOR_DICT_GOODS, values))
        try:
            work_data = read_file_pickle(NAME_FILE_DB_GOODS)
        except FileNotFoundError:
            write_file_pickle(NAME_FILE_DB_GOODS, filds)
        except EOFError:
            if self.name_document == NAME_DOCUMENTS[0]:
                write_file_pickle(NAME_FILE_DB_GOODS, filds)
        else:
            if isinstance(work_data, list):
                work_lst = [data for data in work_data]
            else:
                work_lst = [work_data]
            return work_lst

    def __price_sales(self):
        price_sales_goods = self.price
        rest_partion = self.amount
        num_document = self.number_document
        list_data_from_db = self.__work_method_get_data_from_db()
        if list_data_from_db:
            for i in list_data_from_db:
                if (str(i[PARAMETRS_FOR_DICT_GOODS[1]]) == str(self.name_goods)
                        and i[PARAMETRS_FOR_DICT_GOODS[0]] == NAME_DOCUMENTS[0]
                        and float(i[PARAMETRS_FOR_DICT_GOODS[4]]) != 0.0):
                    price_sales_goods = (str(float(i[PARAMETRS_FOR_DICT_GOODS[3]]) +
                                             float(i[PARAMETRS_FOR_DICT_GOODS[3]]) * float(MARKUP)))
                    rest_partion = str(float(i[PARAMETRS_FOR_DICT_GOODS[4]]))
                    num_document = i[PARAMETRS_FOR_DICT_GOODS[6]]
                    break
        return price_sales_goods, rest_partion, num_document

    def coming(self):
        num_document = self.number_document
        num_document += 1
        list_data_from_db = self.__work_method_get_data_from_db()
        if list_data_from_db:
            metka = 0
            for i in list_data_from_db:
                if (i[PARAMETRS_FOR_DICT_GOODS[1]] == self.name_goods
                        and float(i[PARAMETRS_FOR_DICT_GOODS[3]]) == float(self.price)
                        and i[PARAMETRS_FOR_DICT_GOODS[5]] == self.new_date
                        and i[PARAMETRS_FOR_DICT_GOODS[0]] == NAME_DOCUMENTS[0]):
                    metka = 1
                    i[PARAMETRS_FOR_DICT_GOODS[2]] = str(float(i[PARAMETRS_FOR_DICT_GOODS[2]]) + float(self.amount))
                    i[PARAMETRS_FOR_DICT_GOODS[4]] = str(float(i[PARAMETRS_FOR_DICT_GOODS[4]]) + float(self.amount))
            if metka == 1:
                write_file_pickle(NAME_FILE_DB_GOODS, list_data_from_db)
            else:
                last_num_doc = num_document
                rest_partion = self.amount
                values = [self.name_document, self.name_goods, self.amount, self.price, rest_partion,
                          self.new_date, last_num_doc]
                work_fild = dict(zip(PARAMETRS_FOR_DICT_GOODS, values))
                list_data_from_db.append(work_fild)
                write_file_pickle(NAME_FILE_DB_GOODS, list_data_from_db)
        print(self.__work_method_get_data_from_db())

    def sales(self):
        list_data_from_db = self.__work_method_get_data_from_db()
        price_g, rest_partion, number_doc = self.__price_sales()
        if number_doc != 0:
            if list_data_from_db:
                if float(self.amount) <= float(rest_partion):
                    for j in list_data_from_db:
                        if int(j[PARAMETRS_FOR_DICT_GOODS[6]]) == int(number_doc):
                            j[PARAMETRS_FOR_DICT_GOODS[4]] = str(float(j[PARAMETRS_FOR_DICT_GOODS[4]]) -
                                                                 float(self.amount))
                            rest_partion = j[PARAMETRS_FOR_DICT_GOODS[4]]
                    values = [self.name_document, self.name_goods, self.amount, price_g, rest_partion,
                              self.new_date, number_doc]
                    work_fild = dict(zip(PARAMETRS_FOR_DICT_GOODS, values))
                    list_data_from_db.append(work_fild)
                    write_file_pickle(NAME_FILE_DB_GOODS, list_data_from_db)
                else:
                    print("Количество товара по заданой цене партии завышено")
        else:
            print(f"Необходимо создать документ прихода товара {self.name_goods}")
        print(self.__work_method_get_data_from_db())

    @staticmethod
    def report(key_report_str, key_report_end):
        try:
            work_data = read_file_pickle(NAME_FILE_DB_GOODS)
        except (FileNotFoundError, EOFError):
            print("Нет данных для отображения")
        else:
            if isinstance(work_data, list):
                work_lst = [data for data in work_data]
            else:
                work_lst = [work_data]
            summ_arrival_goods = 0.0
            summ_consum_goods = 0.0
            profit_all = 0.0
            for j in work_lst:
                if (j[PARAMETRS_FOR_DICT_GOODS[0]] == NAME_DOCUMENTS[0]
                        and (j[PARAMETRS_FOR_DICT_GOODS[5]] == key_report_str or
                             j[PARAMETRS_FOR_DICT_GOODS[5]] > key_report_str)
                        and j[PARAMETRS_FOR_DICT_GOODS[5]] <= key_report_end):
                    summ_arrival_goods += float(j[PARAMETRS_FOR_DICT_GOODS[2]]) * float(j[PARAMETRS_FOR_DICT_GOODS[3]])
                if (j[PARAMETRS_FOR_DICT_GOODS[0]] == NAME_DOCUMENTS[1]
                        and (j[PARAMETRS_FOR_DICT_GOODS[5]] == key_report_str or
                             j[PARAMETRS_FOR_DICT_GOODS[5]] > key_report_str)
                        and j[PARAMETRS_FOR_DICT_GOODS[5]] <= key_report_end):
                    summ_consum_goods += float(j[PARAMETRS_FOR_DICT_GOODS[2]]) * float(j[PARAMETRS_FOR_DICT_GOODS[3]])
                    num_doc_partiya = j[PARAMETRS_FOR_DICT_GOODS[6]]
                    amount_consumm = float(j[PARAMETRS_FOR_DICT_GOODS[2]])
                    for k in work_lst:
                        if (k[PARAMETRS_FOR_DICT_GOODS[0]] == NAME_DOCUMENTS[0]
                                and k[PARAMETRS_FOR_DICT_GOODS[6]] == num_doc_partiya):
                            profit_all += amount_consumm * float(k[PARAMETRS_FOR_DICT_GOODS[3]])
            profit = round(summ_consum_goods - profit_all, 2)
            print(f"Итого:  {summ_arrival_goods}   |  {summ_consum_goods}    |  {profit}    |\n")
            print("-----------------------------------------\n")


def number_document():
    last_numb_doc = 0
    try:
        lst_data_from_db = read_file_pickle(NAME_FILE_DB_GOODS)
    except FileNotFoundError:
        print("Файл отсутствует в директории")
    except EOFError:
        last_numb_doc = 0
    else:
        if isinstance(lst_data_from_db, list):
            if len(lst_data_from_db) > 0:
                last_numb_doc = max([i[PARAMETRS_FOR_DICT_GOODS[6]] for i in lst_data_from_db])
            else:
                last_numb_doc = 0
        else:
            last_numb_doc = lst_data_from_db[PARAMETRS_FOR_DICT_GOODS[6]]
    return last_numb_doc


def menu_about_goods_coming():
    print("Введите данные о товаре:")
    date_action = input("Дата в формате 'dd-mm-yyyy': ")
    name_goods = input("Наименование: ")
    amount_goods = input("Количество в формате '0.00': ")
    price_goods = input("Цена в формате '0.00': ")
    return date_action, name_goods, amount_goods, price_goods


def menu_about_goods_sales():
    print("Введите данные о товаре:")
    date_action = input("Дата в формате 'dd-mm-yyyy': ")
    name_goods = input("Наименование: ")
    amount_goods = input("Количество в формате '0.00': ")
    return date_action, name_goods, amount_goods


def main_menu():
    action = input("1. Приход товара\n"
                   "2. Продажа товара\n"
                   "3. Отчет за период\n"
                   "Выберите действие, которое необходимо выполнить: ")
    if action == "1":
        dt_action, nm_goods, am_goods, pr_goods = menu_about_goods_coming()
        num_doc = number_document()
        if (pattern_dates(dt_action) or dt_action == '') and pattern_float_numbers(pr_goods) \
                and float(pr_goods) != 0.0 and pattern_float_numbers(am_goods):
            if dt_action == '':
                dt_action = datetime.datetime.now().strftime("%d-%m-%Y")
            new_goods = AccountingForGoodsStore(NAME_DOCUMENTS[0], nm_goods, am_goods, pr_goods, dt_action, num_doc)
            new_goods.coming()
        else:
            print("Не корректный формат данных")
    elif action == "2":
        dt_action, nm_goods, am_goods = menu_about_goods_sales()
        num_doc = 0
        price = '0.0'
        if pattern_dates(dt_action) or dt_action == '' and pattern_float_numbers(am_goods):
            if dt_action == '':
                dt_action = datetime.datetime.now().strftime("%d-%m-%Y")
            new_goods = AccountingForGoodsStore(NAME_DOCUMENTS[1], nm_goods, am_goods, price, dt_action, num_doc)
            new_goods.sales()
    elif action == "3":
        print("Выберите период отчета для отображения на экране: \n")
        key_report_start = input("Дата начала периода: ")
        key_report_end = input("Дата конец периода: ")
        if pattern_dates(key_report_start) and pattern_dates(key_report_end):
            print(f"Отчет за период {key_report_start} - {key_report_end}: \n")
            print("----------------------------------------\n")
            print(f"       Приход   |  Расход  |  Прибыль  |\n")
            AccountingForGoodsStore.report(key_report_start, key_report_end)
        else:
            print("Некорректный формат даты")
    else:
        print("Некорректно выбранное действие")


main_menu()
