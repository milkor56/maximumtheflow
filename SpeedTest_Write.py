import pyspeedtest, gspread
from oauth2client.service_account import ServiceAccountCredentials
from Logger import log
from datetime import datetime


def get_gsheet_dict(sheet):
    sheet_dict = {}
    count = 1
    while count < sheet.col_count:
        colheader = str(sheet.cell(1, count))
        sheet_dict[colheader[colheader.find("'")+1: colheader.find("'", colheader.find("'") + 1)]] = count
        count += 1

    return sheet_dict


if __name__ == '__main__':
    log(datetime.today())

    st_arry = []

    dt = datetime.today()

    st = pyspeedtest.SpeedTest()

    if dt.hour > 12:
        hour = dt.hour - 12
        ampm = "PM"
    elif dt.hour == 12:
        hour = 12
        ampm = "PM"
    elif dt.hour == 0:
        hour = 12
        ampm = "AM"
    else:
        hour = dt.hour
        ampm = "AM"
    if len('%s' % dt.minute) == 1:
        str_time = '%s:0%s %s' % (hour, dt.minute, ampm)
    else:
        str_time = '%s:%s %s' % (hour, dt.minute, ampm)

    st_arry.append('%s/%s/%s %s' % (dt.month, dt.day, dt.year, str_time))
    st_arry.append('%s/%s/%s' % (dt.month, dt.day, dt.year))
    st_arry.append(str_time)
    st_arry.append(st.ping())
    st_arry.append(st.download() / 1024 / 1024)
    st_arry.append(st.upload() / 1024 / 1024)
    st_arry.append(60)

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\git\not_in_git\maximumtheflow.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Spectrum SpeedTest").sheet1

    sheet_rows = sheet.get_all_records()

    sheet_dict = get_gsheet_dict(sheet=sheet)

    sheet.insert_row(st_arry, index=len(sheet_rows)+2)

    # print st_arry

    # sheet.update_cell(count, sheet_dict['Date'], st_arry['Date'])

    log("DONE!")
    log(datetime.today())
