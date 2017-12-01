import pygsheets


class GoogleSheets(object):
    def __init__(self, sheet_name):
        gc = pygsheets.authorize(service_file='../config/google_api_secrets.json')
        self.spreadsheet = gc.open(sheet_name)

    def get_spreadsheet(self):
        return self.spreadsheet