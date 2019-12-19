import datetime
import unittest
from unittest.mock import patch
from Main_file import AccountingForGoodsStore
from Main_file import menu_about_goods_coming
from Main_file import menu_about_goods_sales
from Main_file import number_document
from Read_files import read_file_pickle
from Read_files import write_file_pickle


class TestAccountingForGoodsStore(unittest.TestCase):
    def test_regex_date(self):
        date_example = "\d{2}-\d{2}-\d{4}"
        self.assertRegex("01-01-2019", date_example, "Correct date")
        self.assertNotRegex("01-1-2019", date_example, "Invalid date")
        self.assertNotRegex("1-10-2019", date_example, "Invalid date")
        self.assertNotRegex("01-01-19", date_example, "Invalid date")
        self.assertNotRegex("1-1-2019", date_example, "Invalid date")
        self.assertNotRegex("1-1-19", date_example, "Invalid date")

    def test_regex_price_amount(self):
        price_amount_example = "^\d*\.\d+$"
        self.assertRegex("10.2", price_amount_example, "Сorrect input")
        self.assertRegex("10.22", price_amount_example, "Сorrect input")
        self.assertRegex("1.22", price_amount_example, "Сorrect input")
        self.assertNotRegex("-2.22", price_amount_example, "Incorrect input")
        self.assertNotRegex("2.-22", price_amount_example, "Incorrect input")
        self.assertNotRegex("-22", price_amount_example, "Incorrect input")
        self.assertNotRegex("-22.", price_amount_example, "Incorrect input")
        self.assertNotRegex("22", price_amount_example, "Incorrect input")
        self.assertNotRegex("2.", price_amount_example, "Incorrect input")

    def test_type_value_more_then_one(self):
        values_coming = menu_about_goods_coming()
        values_sales = menu_about_goods_sales()
        self.assertIsInstance(values_coming, tuple, "Valid return type")
        self.assertIsInstance(values_sales, tuple, "Valid return type")
        self.assertNotIsInstance(values_coming, str, "Invalid return type")
        self.assertNotIsInstance(values_sales, str, "Invalid return type")
        self.assertNotIsInstance(values_coming, list, "Invalid return type")
        self.assertNotIsInstance(values_sales, list, "Invalid return type")
        self.assertNotIsInstance(values_coming, dict, "Invalid return type")
        self.assertNotIsInstance(values_sales, dict, "Invalid return type")

    def test_type_value(self):
        value = number_document()
        self.assertIsInstance(value, int, "Valid return type")
        self.assertNotIsInstance(value, float, "Invalid return type")

    @patch("pickle.load")
    def test_read_file_pickle(self, load):
        read_file_pickle("goods_db")
        self.assertTrue(load.called)

    @patch("pickle.dump")
    def test_write_file_pickle(self, dump):
        write_file_pickle("goods_db", "some_text")
        self.assertTrue(dump.called)

    def test_IsInstance_AccountingForGoodsStore(self):
        new_object = AccountingForGoodsStore("Name document", "Name goods", "Amount", "Price", "Date document", 0)
        self.assertIsInstance(new_object, AccountingForGoodsStore, "Class object AccountingForGoodsStore")

    @patch('Main_file.AccountingForGoodsStore.coming', return_value=True)
    def test_coming(self, coming):
        self.assertEqual(coming(), True)

    @patch('Main_file.AccountingForGoodsStore.sales', return_value=True)
    def test_sales(self, sales):
        self.assertEqual(sales(), True)

    @patch('Main_file.AccountingForGoodsStore.report', return_value=2)
    def test_report(self, report):
        date_one = datetime.datetime.now().strftime("%d-%m-%Y")
        date_two = datetime.datetime.now().strftime("%d-%m-%Y")
        self.assertEqual(report(date_one, date_two), 2)


if __name__ == '__main__':
    unittest.main()
