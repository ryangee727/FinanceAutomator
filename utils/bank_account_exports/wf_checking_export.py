from utils.bank_account_exports.bank_export import BankExport


class WFCheckingExport(BankExport):
    def __init__(self, export_file):
        BankExport.__init__(self, export_file)
        self.exclude_keywords = [
            'Acorns',
            'VENMO',
            'BILL PAY',
            'CAPITALONE',
            'ATM',
            'BARCLAYCARD',
            'CFBurling',
            'CARDMEMBER'
        ]
        self.format_data()

    def format_data(self):
        self.extract_to_data_frame(names=['Date', 'Price', 'Del1', 'Del2', 'Name'])
        self.rename_column('Description', 'Name')
        self.remove_column('Del1')
        self.remove_column('Del2')
        self.remove_rows_with_excluded_words(self.exclude_keywords)
        super().format_data()

