from utils.google_sheets import GoogleSheets
from dateutil.relativedelta import *
from utils.util import isfloat, convert_float_to_dollar
import datetime


class ConsciousSpendingPlan(object):
    def __init__(self):
        self.spreadsheet = GoogleSheets("Conscious Spending Plan").get_spreadsheet()
        self.prev_month = (datetime.datetime.now() + relativedelta(months=-2)).strftime('%b')
        self.prev_months_year = (datetime.datetime.now() + relativedelta(months=-2)).strftime('%y')
        self.year = (datetime.datetime.now() + relativedelta(months=-1)).strftime('%y')
        self.month = (datetime.datetime.now() + relativedelta(months=-1)).strftime('%b')
        self.next_month = datetime.datetime.now().strftime('%b')
        self.next_months_year = datetime.datetime.now().strftime('%y')
        self.wksheet_name = self.month + " '{}".format(self.year)
        self.next_wksheet_name = self.next_month + " '{}".format(self.next_months_year)
        self.current_wksht = self.spreadsheet.worksheet_by_title(self.wksheet_name)
        self.next_wksheet = None

    @staticmethod
    def __split_shared_cost_row(row):
        if row['Shared?'] in ['y', 'AE']:
            return convert_float_to_dollar(float(row['Price'][2:].replace(',', '')) / 2.0)
        elif isfloat(row['Shared?']):
            return convert_float_to_dollar(row['Shared?'])
        else:
            return row['Cost']

    def __split_shared_costs(self, df):
        df['Cost'] = df.apply(lambda row: self.__split_shared_cost_row(row), axis=1)
        return df

    def import_df(self, df):
        print("Importing Data into {}".format(self.wksheet_name))
        df = df[['Date', 'Name', 'Category', 'Price', 'Cost', 'Shared?']]
        self.current_wksht.set_dataframe(df, (5, 1), copy_head=False)

    def export_df_split_shared(self):
        return self.__split_shared_costs(self.current_wksht.get_as_df(start='A4', end='F87'))

    def export_shared_only_df(self):
        df = self.export_df_split_shared()
        return df[(df['Shared?'] != '')]  # & (df['Shared?'] != 'AE') To remove AE expenses from export

    def export_csv_for_training_data(self):
        df = self.export_df_split_shared()
        df.to_csv('../data/training_data/test.csv', index=False)

    def update_worksheet_with_split_shared(self):
        self.import_df(self.export_df_split_shared())

    def add_next_months_worksheet(self):
        try:
            self.spreadsheet.add_worksheet(self.next_wksheet_name, src_worksheet=self.current_wksht)
            self.next_wksheet = self.spreadsheet.worksheet_by_title(self.next_wksheet_name)
            self.__modify_next_months_worksheet()
        except Exception as e:
            print(e)

    def __modify_next_months_worksheet(self):
        cells = self.__get_cells_to_update().items()
        for cell_loc, cell in cells:
            formula_month_replaced = cell.formula.replace(self.prev_month, self.month)
            self.next_wksheet.update_cell(cell_loc, formula_month_replaced)
            self.next_wksheet.update_cell(cell_loc, formula_month_replaced.replace(self.prev_months_year, self.year))

    def __get_cells_to_update(self):
        cells = {}
        for cell in ['B1','D1','F1','H1','J1','L1']:
            cells[cell] = self.next_wksheet.cell(cell)
        return cells
