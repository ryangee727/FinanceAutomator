from utils.bank_account_exports.bank_export import BankExport


class BarclaycardExport(BankExport):
    def __init__(self, export_file):
        BankExport.__init__(self, export_file)
        self.format_data()

    def format_data(self):
        self.extract_to_data_frame(skip_rows=3)
        self.rename_column('Description', 'Name')
        self.rename_column('Transaction Date', 'Date')
        self.rename_column('Amount', 'Price')
        self.remove_payments()
        self.create_cost_column()
        self.create_category_column()
        self.filter_monthly_costs()

