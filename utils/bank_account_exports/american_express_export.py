from utils.bank_account_exports.bank_export import BankExport


class AmericanExpressExport(BankExport):
    def __init__(self, export_file):
        BankExport.__init__(self, export_file)
        self.format_data()

    def format_data(self):
        self.extract_to_data_frame(names=['Date', 'Del1', 'Price', 'Name', 'Del2'])
        self.remove_column('Del1')
        self.remove_column('Del2')
        super().format_data(american_express_expenses=True)

