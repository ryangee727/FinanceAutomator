import pandas as pd
import numpy as np


class BankExport(object):
    def __init__(self, export_file):
        self.export_file = export_file
        self.data_frame = None

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
        df = pd.read_csv(self.export_file, skiprows=skip_rows)
        self.data_frame = df

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

