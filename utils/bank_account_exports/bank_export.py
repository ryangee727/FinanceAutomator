import pandas as pd
import numpy as np
from dateutil.relativedelta import *
import datetime


class BankExport(object):
    def __init__(self, export_file):
        self.export_file = export_file
        self.day_one_last_month = (datetime.date.today() + relativedelta(months=-1)).replace(day=1).strftime('%m/%d/%Y')
        self.day_one_cur_month = datetime.date.today().replace(day=1).strftime('%m/%d/%Y')
        self.data_frame = None

    def _str_to_pd_date(self, date_str):
        return pd.to_datetime(date_str, format='%m/%d/%Y')

    def _convert_date_column(self):
        self.data_frame['Date'] = self._str_to_pd_date(self.data_frame['Date'])

    def _convert_date_back_to_string(self):
        self.data_frame['Date'] = self.data_frame['Date'].dt.strftime('%m/%d/%Y')

    def is_barclaycard_export(self):
        return 'CreditCard_' in self.export_file

    def is_rei_export(self):
        return 'export' in self.export_file

    def get_bank_type(self):
        if self.is_barclaycard_export():
            return 'Barclaycard'
        elif self.is_rei_export():
            return 'REI'

    def extract_to_data_frame(self, skip_rows=0):
        self.data_frame = pd.read_csv(self.export_file, skiprows=skip_rows)

    def remove_column(self, col_name):
        self.data_frame.drop(col_name, axis=1, inplace=True)

    def rename_column(self, col_name, new_name):
        self.data_frame.rename(columns={col_name: new_name}, inplace=True)

    def remove_payments(self):
        self.data_frame = self.data_frame[self.data_frame.Price <= 0]

    def create_cost_column(self):
        self.data_frame['Cost'] = np.absolute(self.data_frame.Price)

    def create_category_column(self):
        self.data_frame['Category'] = 'Eating Out'

    def filter_monthly_costs(self):
        self._convert_date_column()
        filter_on_date = self.data_frame[
            (self.data_frame['Date'] >= self._str_to_pd_date(self.day_one_last_month)) &
            (self.data_frame['Date'] < self._str_to_pd_date(self.day_one_cur_month))
        ]
        self.data_frame = filter_on_date
        self._convert_date_back_to_string()

    def format_data(self):
        self.remove_payments()
        self.create_cost_column()
        self.create_category_column()
        self.filter_monthly_costs()



