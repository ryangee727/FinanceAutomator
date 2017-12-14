from utils.google_sheets import GoogleSheets
from dateutil.relativedelta import *
import datetime


class ARExpenses(object):
    def __init__(self):
        self.spreadsheet = GoogleSheets("A&R Expenses").get_spreadsheet()
        self.year = (datetime.datetime.now() + relativedelta(months=-1)).strftime('%y')
        self.month = (datetime.datetime.now() + relativedelta(months=-1)).strftime('%b')
        self.next_month = datetime.datetime.now().strftime('%b')
        self.next_month_full_name = datetime.datetime.now().strftime('%B')
        self.next_months_year = datetime.datetime.now().strftime('%y')
        self.wksheet_name = self.month + " '{}".format(self.year)
        self.next_wksheet_name = self.next_month + " '{}".format(self.next_months_year)
        self.current_wksht = self.spreadsheet.worksheet_by_title(self.wksheet_name)
        self.next_wksheet = None

    def __format_df(self, df):
        df['Paid By'] = 'Ryan'
        df['Blank'] = ''
        df['Price'] = df.apply(lambda row: row['Price'][1:], axis=1)
        df['Category'] = df.apply(lambda row: self.__convert_categories(row['Category']), axis=1)
        df = df[['Date', 'Category', 'Name', 'Price', 'Paid By', 'Blank', 'Cost']]
        return df

    @staticmethod
    def __convert_categories(category):
        category_conversion = {
            'Groceries': 'Grocery',
            'Eating Out': 'Restaurant',
            'Fixed': 'Utilities'
        }
        return category_conversion[category] if category in category_conversion else category

    def get_last_row_number(self):
        return len(self.current_wksht.get_all_values()) + 1

    def import_df(self, df):
        df = self.__format_df(df)
        self.current_wksht.set_dataframe(df, (self.get_last_row_number(), 1), copy_head=False)

    def add_next_months_worksheet(self):
        try:
            self.spreadsheet.add_worksheet(self.next_wksheet_name, src_worksheet=self.current_wksht)
            self.next_wksheet = self.spreadsheet.worksheet_by_title(self.next_wksheet_name)
            self.__modify_next_months_worksheet()
        except Exception as e:
            print(e)

    def __modify_next_months_worksheet(self):
        self.next_wksheet.clear('A8', 'J{}'.format(str(self.get_last_row_number())))
        self.next_wksheet.update_cell('A1', '{} EXPENSES'.format(self.next_month_full_name.upper()))

