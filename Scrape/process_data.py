#############
# Notes:
# Working on data processing. Seem to have gotten opening and closing trades aligned properly
# however position adjustment are showing to the right of other closing trades. Will need to
# concat position adjustmens and closing trades before join.
#############

import pandas as pd
import numpy as np
import sqlite3
import datetime
from datetime import timedelta
from datetime import datetime, date
from dateutil import parser


def process():
    conn = sqlite3.connect('raw_data.db')
    c = conn.cursor()

    df_raw = pd.read_sql('SELECT * FROM raw_data', conn, index_col=None)
    conn.close()

process()
    # df_raw = pd.DataFrame(df_pull, columns=['First'])
    # df_raw.to_csv('df_test.csv')
#     df = pd.DataFrame(df_raw.values.reshape(-1, 11), columns=[
#         'Type', 'Trade Date', 'Settle Date', 'Symbol', 'Description', 'Trade Action', 'Qty', 'Price', 'Fees', 'Commision', 'Net Amount'
#     ])
#
#     df_close = (df.loc[df['Trade Action'].isin(['Sell To Close', 'Buy To Close'])])
#     df_open = (df.loc[df['Trade Action'].isin(['Sell To Open', 'Buy To Open'])])
#     df_move = (df.loc[df['Type'].isin(['Money Movements'])])
#
#     df_positions = (df.loc[df['Type'].isin(['Position Adjustments'])])
#
#     df_positions = df_positions.rename(columns={
#         'Type': 'Type_y', 'Trade Date': 'Trade Date_y', 'Settle Date': 'Settle Dat_y', 'Symbol': 'Symbol_y',
#         'Description': 'Description_y', 'Trade Action': 'Trade Action_y', 'Qty': 'Qty_y', 'Price': 'Price_y',
#         'Fees': 'Fees_y', 'Commision': 'Commision_y', 'Net Amount': 'Net Amount_y'
#     })
#
#     df_close = df_close.rename(columns={
#         'Type': 'Type_x', 'Trade Date': 'Trade Date_x', 'Settle Date': 'Settle Dat_x', 'Symbol': 'Symbol_x',
#         'Description': 'Description_x', 'Trade Action': 'Trade Action_x', 'Qty': 'Qty_x', 'Price': 'Price_x',
#         'Fees': 'Fees_x', 'Commision': 'Commision_x', 'Net Amount': 'Net Amount_x'
#     })
#
#     result = pd.concat([df_open, df_close, df_positions], axis=1, sort=False)
#     df_close = result.filter([
#         'Type_x', 'Trade Date_x', 'Settle Date_x', 'Symbol_x', 'Description_x', 'Trade Action_x', 'Qty_x', 'Price_x', 'Fees_x', 'Commision_x',
#         'Net Amount_x'
#     ])
#
#     df_position = result.filter([
#         'Type_y', 'Trade Date_y', 'Settle Date_y', 'Symbol_y', 'Description_y', 'Trade Action_y', 'Qty_y', 'Price_y', 'Fees_y',
#         'Commision_y', 'Net Amount_y'
#     ])
#
#     df_position = df_position.rename(columns={
#         'Type_y': 'Type_x', 'Trade Date_y': 'Trade Date_x', 'Settle Date_y': 'Settle Dat_x', 'Symbol_y': 'Symbol_x',
#         'Description_y': 'Description_x', 'Trade Action_y': 'Trade Action_x', 'Qty_y': 'Qty_x', 'Price_y': 'Price_x',
#         'Fees_y': 'Fees_x', 'Commision_y': 'Commision_x', 'Net Amount_y': 'Net Amount_x'
#     })
#
#     df_close = df_close.set_index('Symbol_x', inplace=False)
#
#     df_position = df_position.set_index('Symbol_x', inplace=False)
#     df_close = pd.concat([df_position, df_close])
#     df_open = df_open.join(df_close, on=['Symbol'])
#     # df_open2 = df_open1.join(position1, on=['Symbol'])
#     # df_result = pd.concat([df_open, df_move])
#     df_final = df_open.set_index('Trade Date', inplace=False)
#     #
#     # # df.to_sql('processed_data', conn, if_exists='replace', index=False)
#     #
#     # df_close.to_csv('df_test1.csv')
#     df_final = df_final.drop_duplicates()
#     # df_final.to_csv('df_test.csv')
#     # print(df)
#
#     # df_final[df.columns[7:11]] = df_final[df.columns[7:11]].replace('[\$,)]', '', regex=True)
#     # df_final[df.columns[7:11]] = df_final[df.columns[7:11]].replace('\(', '-', regex=True).astype(float)
#     #
#     # df_final[df.columns[10:25]] = df_final[df.columns[10:25]].replace('[\$,)]', '', regex=True)
#     # df_final[df.columns[10:25]] = df_final[df.columns[10:25]].replace('\(', '-', regex=True).astype(float)
#
#     # # # # # # # #
#     # Format numbers
#     # # # # # # # #
#
#     cols = [
#         'Qty', 'Price', 'Fees', 'Commision', 'Net Amount',
#         'Qty_x', 'Fees_x', 'Commision_x',
#         'Net Amount_x'
#     ]
#
#     df_final[cols] = df_final[cols].replace({'[$]': '', "[(]": '-', '[)]': ''}, regex=True)
#
#     # print(df_final)
#     df_final[[
#         'Qty', 'Price', 'Fees', 'Commision', 'Net Amount',
#         'Qty_x', 'Fees_x', 'Commision_x',
#         'Net Amount_x'
#     ]] = df_final[[
#         'Qty', 'Price', 'Fees', 'Commision', 'Net Amount',
#         'Qty_x', 'Fees_x', 'Commision_x',
#         'Net Amount_x'
#     ]].apply(pd.to_numeric)
#
#     # # # # # # # #
#     # Add profit column
#     # # # # # # # #
#
#     profit_col = df_final['Net Amount'] + df_final['Net Amount_x']  # Need to convert columns to intergers or floats!
#     df_final['Net Profit'] = profit_col
#
# # df_final.to_csv('df_test.csv')
#
# # df_final['Trade Date_x'] = pd.to_datetime(df['Trade Date_x'], format='%m/%d/%Y')
#
# # # # # # # # #
# # Add previous week df
# # # # # # # # #
#
# # today = datetime.date.today()
# today = date(2020, 4, 26)
# weekday = today.weekday()
# start_delta = timedelta(days=weekday, weeks=1)
# start_of_week = today - start_delta
#
# print(start_of_week)
#
# week_dates = []
# x = 0
# while x < 7:
#     # week_dates.append(start_of_week + timedelta(days=x))
#     ddd = [str(start_of_week + timedelta(days=x))]
#     week_dates.append(ddd)
#     x += 1
#
# # df_week = (df.loc[df_final['Trade Date_x'].isin([f'{week_dates}'])])
# # print(week_dates)
# # week_dates = [str(i) for i in week_dates]
# # week_dates = [str(i) for i in week_dates]
# # date_strings = [d.strftime('%m-%d-%Y') for d in week_dates]
#
# df_dates = pd.DataFrame(week_dates, columns=['Date'])
#
# # objDate = datetime.strptime(week_dates, '%Y, %m, %d')
#
# df_dates['Date'] = pd.to_datetime(df_dates['Date'])
# df_dates = df_dates["Date"].dt.strftime("%#m/%#d/%Y")
# # dates = df_dates.values.tolist()
# # test = df_final['Trade Date_x'].values.tolist()
# # df_test = (df.loc[df_final['Trade Date_x'].isin([dates])])
# # df_final['Trade Date_x'] = df_final['Trade_Date_x'].astype(int)
# # df_final['Trade Date_x'] = datetime.strptime(df_final['Trade Date_x'], '%Y, %m, %d')
# df_final['Trade Date_x'] = pd.to_datetime(df_final['Trade Date_x'], format='%m/%d/%y')
# df_1 = df_final[df_final['Trade Date_x'] <= '4/3/2020']
#
# # print(df_1)
#
# df_1.to_csv('df_1.csv')
# # print('test', test)
# # print('dates', dates)
# # # dates = df_dates.values.tolist()
# # i1 = df_final.set_index('4/3/20').index
# # i2 = df_dates.set_index(dates).index
# # # print(i2)
# # print(df_final[i1.isin(i2)])
# # print(filtered_df)
