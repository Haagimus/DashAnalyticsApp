import base64
import io
from datetime import date, datetime, timedelta
from math import floor

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

from assets.SQL import add_time_entry_df, get_rows
from assets.models import Functions
from server import app, log_time
import assets.callbacks


# TODO: add controls to view and edit charge codes, major programs and projects

def fiscal_year_start(year):
    year -= 1
    if year < 2019:
        return date(year, 12, 31) + timedelta(1)
    else:
        prev_friday = date(year, 12, 31) - timedelta(days=date(year, 12, 31).weekday() + 3)
        next_friday = date(year, 12, 31) + timedelta(days=- date(year, 12, 31).weekday() - 3, weeks=1)
        dates = [prev_friday, next_friday]

        return min(dates, key=lambda d: abs(d - date(year, 12, 31))) + timedelta(1)


def pdcalc(year, month, day):
    fofy = fiscal_year_start(year)
    delta = date(year, month, day) - fofy
    week_num = floor(delta.days / 7) + 1
    currentwk = 1
    # Iterate through all the months
    for m in range(1, 13):
        # The current month is one of the 5 week months
        if m % 3 == 0:
            subpd = 1
            prevwk = currentwk
            currentwk += 5
            for i in range(prevwk, currentwk):
                if i == week_num:
                    return {'Period': m, 'Sub-Period': subpd, 'Week Number': week_num}
                subpd += 1
        # The current month is one of the 4 week months
        else:
            subpd = 1
            prevwk = currentwk
            currentwk += 4
            for i in range(prevwk, currentwk):
                if i == week_num:
                    return {'Period': m, 'Sub-Period': subpd, 'Week Number': week_num}
                subpd += 1


def parse_contents(contents, filename, data):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8)))')), header=None)
        elif 'xls' in filename:
            # Assume the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=None)
    except Exception as e:
        app.logger.error(f'ERROR :: [{e.errno}] :: {e.strerror} at {log_time}')
        return html.Div(['There was an error processing this file.'])

    # https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
    # this link provides good reference on retrieving data from a dataframe
    # This section processes the data contained within the SUMMARY worksheet of the uploaded workbook
    pgm_data = df.loc[:5, {0, 2, 4}]
    i = {1}
    i.update({n for n in range(10, 46)})
    summary_data = df.loc[7:30, i]

    charge_num = pgm_data.iloc[1, 1].split('.')[0]
    func_table = [[f.finance_function, f.function] for f in get_rows(Functions)]

    table = []
    try:
        for col in range(summary_data.shape[1]):
            for row in range(summary_data.shape[0]):
                if col == summary_data.shape[1] - 1 and 6 <= row <= 23:
                    for i in range(1, summary_data.shape[1]):
                        parsed_date = datetime.strptime(summary_data.iloc[2, i][4:], '%b-%y').date()
                        pd_info = pdcalc(parsed_date.year, parsed_date.month, 15)

                        func = [x[1] for x in func_table if x[0] == summary_data.iloc[row, 0]][0]
                        table.append(
                            [f'{charge_num}-{summary_data.iloc[0, i]}-{pd_info["Period"]}-{pd_info["Sub-Period"]}-{func}',
                             # psuedo-index
                             summary_data.iloc[0, i],  # year
                             pd_info['Period'],  # period
                             pd_info['Sub-Period'],  # sub_period
                             summary_data.iloc[1, i],  # quarter
                             summary_data.iloc[2, i][4:],  # month
                             summary_data.iloc[row, i],  # hours
                             charge_num,  # charge_number
                             func])  # function

        sheet_data = pd.DataFrame(table, columns=['uid', 'year', 'period', 'sub_period', 'quarter', 'month', 'hours',
                                                  'charge_number', 'function_name'])
        add_time_entry_df(sheet_data)

        # This section processes the data contained within the NEEDS worksheet of the uploaded workbook

        app.logger.info(f'INFO :: file {filename} was imported by {data["login_user"]} at {log_time}')
    except Exception as e:
        print(e)

def program_page_layout():
    layout = html.Div(id='programs-page-container')

    return layout
