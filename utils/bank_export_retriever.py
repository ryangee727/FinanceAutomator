import glob
from utils.bank_account_exports.bank_account_export_factory import BankAccountExportFactory


class BankExportRetriever(object):
    def __init__(self, export_folder):
        self.export_folder = export_folder
        self.bank_exports = []
        self.populate_bank_exports_list()

    def populate_bank_exports_list(self):
        for export in glob.glob(self.export_folder + '*.csv'):
            bank_export = BankAccountExportFactory(export).produce()
            if bank_export:
                self.bank_exports.append(bank_export.data_frame)

    def get_bank_exports(self):
        return self.bank_exports
