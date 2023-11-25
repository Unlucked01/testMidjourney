import gspread
from oauth2client.service_account import ServiceAccountCredentials

table_name = 'Промпт бота для картинок'


def read():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(table_name)

    all_sheets = spreadsheet.worksheets()

    first_sheet = all_sheets[0]
    cell_value = first_sheet.cell(2, 1).value
    return cell_value



