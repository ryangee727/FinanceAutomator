from utils.bank_account_exports.barclaycard_export import BarclaycardExport
from utils.bank_account_exports.rei_export import REIExport
from utils.bank_account_exports.bank_export import BankExport


class BankAccountExportFactory(object):
    def __init__(self, csv_file):
        self.bank_types = {
            'REI': REIExport,
            'Barclaycard': BarclaycardExport
        }
        self.csv_file = csv_file

    def produce(self):
        try:
            bank_type = BankExport(self.csv_file).get_bank_type()
            return self.bank_types[bank_type](self.csv_file)
        except KeyError as e:
            print('{} does not match a bank account type'.format(self.csv_file))
            pass
