from utils.bank_account_exports.bank_export import BankExport


class REIExport(BankExport):
    def __init__(self, export_file):
        BankExport.__init__(self, export_file)
        self.format_data()

    def format_data(self):
        self.extract_to_data_frame()
        self.remove_column('Transaction')
        self.remove_column('Memo')
        self.rename_column('Amount', 'Price')
        super().format_data()

