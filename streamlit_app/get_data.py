import duckdb
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from datetime import datetime


def adjust_data_line(file_path, state, months):
    '''select_and_calculate'''
    data = dataframes[file_path]
    data['month'] = pd.to_datetime(data['month'])
    current_date = pd.to_datetime(datetime.now())
    start_date = current_date - pd.DateOffset(months=months)
    filtered_data = data[(data['State'] == state) &
                         (data['month'] >= start_date) &
                         (data['month'] <= current_date)]

    filtered_data = filtered_data.copy()  # Create a copy
    filtered_data['month'] = pd.to_datetime(
        filtered_data['month']).dt.strftime('%b-%y')
    # Make sure the total column is a floating point number
    filtered_data['total'] = filtered_data['total'].astype(float)

    filtered_data['previous_total'] = filtered_data['total'].shift(1)
    # Calculation of percentage increase.
    filtered_data['percentage_increase'] = ((filtered_data['total'] - filtered_data['previous_total']) /
                                            filtered_data['previous_total']) * 100

    # Clear the NaN value
    filtered_data = filtered_data.dropna(subset=['percentage_increase'])
    return filtered_data[['State', 'month', 'total', 'percentage_increase']]


def adjust_data_area(file_key, state, months):
    """
    Slect and format data.
    """
    data = dataframes[file_key]
    data['month'] = pd.to_datetime(data['month'])
    current_date = pd.to_datetime(datetime.now())
    start_date = current_date - pd.DateOffset(months=months)

    filtered_data = data[(data['State'] == state) &
                         (data['month'] >= start_date) &
                         (data['month'] <= current_date)]
    filtered_data = filtered_data.copy()
    filtered_data['month'] = pd.to_datetime(
        filtered_data['month']).dt.strftime('%b-%y')

    return filtered_data


def adjust_data_radar(file_path, state, start_date, end_date):
    """
    filter_and_format_data for radar charts，Also format the month as ‘January’ style.
    """
    data = dataframes[file_path]
    data['month'] = pd.to_datetime(data['month'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = data[(data['State'] == state) &
                         (data['month'] >= start_date) &
                         (data['month'] <= end_date)]
    filtered_data = filtered_data.copy()
    filtered_data['month'] = pd.to_datetime(
        filtered_data['month']).dt.strftime('%B')  # Converted to full month name

    return filtered_data


def extract_data():
    """
    extract data to csv file.
    """
    load_dotenv()
    PAT = st.secrets['MOTHERDUCK_PAT']
    con = duckdb.connect(f'md:?motherduck_token={PAT}')

    # get total numbers of different companies by state by month
    sql_folder = 'SQL file'
    dataframes = {}
    for sql_file in os.listdir(sql_folder):
        if sql_file.endswith('.sql'):
            file_path = os.path.join(sql_folder, sql_file)

            # Read the SQL query from the file
            with open(file_path, 'r') as f:
                sql_query = f.read()

            # Execute the query and store the result in a DataFrame
            df = con.sql(sql_query).fetchdf()
            # Use the file name as the key
            df_name = os.path.splitext(sql_file)[0]
            dataframes[df_name] = df
            print(f"Data loaded for {df_name}")

    con.close()
    return dataframes


def show_database_info():
    """
    show database and print some data.
    """
    load_dotenv()
    PAT = st.secrets['MOTHERDUCK_PAT']
    con = duckdb.connect(f'md:?motherduck_token={PAT}')
    # check databases, columns
    # my_db.active_private_company
    # my_db.active_public_company
    # my_db.active_sole_trader
    con.sql("SHOW DATABASES").show()
    con.sql("DESCRIBE my_db.active_private_company").show()
    # to print out results
    con.sql("SELECT * FROM my_db.active_private_company LIMIT 10;").show()
    con.sql("SELECT * FROM my_db.active_public_company LIMIT 10;").show()
    con.sql("SELECT * FROM my_db.active_sole_trader LIMIT 10;").show()


dataframes = extract_data()
# dataframes = extract_data()

# extract_data()


# 1. read data
# load_dotenv()
# PAT = os.getenv('MOTHERDUCK_PAT')
# con = duckdb.connect(f'md:?motherduck_token={PAT}')

# ## check databases, columns
# # con.sql("SHOW DATABASES").show()
# # con.sql("DESCRIBE my_db.active_private_company").show()

# # my_db.active_private_company
# # my_db.active_public_company
# # my_db.active_sole_trader

# ## to print out results
# # df = con.sql("SELECT * FROM my_db.active_private_company LIMIT 10;").fetchdf()
# # con.sql("SELECT * FROM my_db.active_private_company LIMIT 10;").show()
# # con.sql("SELECT * FROM my_db.active_public_company LIMIT 10;").show()

# ## to save results to dataframe
# # df = con.sql("SELECT * FROM my_db.active_private_company WHERE ABN = 64600007083;").fetchdf()
# # pd.set_option('display.max_columns', None)
# # print(df.head())

# ## total by state by month for each table
# # con.sql("SELECT state, COUNT(*) as total FROM my_db.active_private_company GROUP BY state;").show()
# # con.sql("SELECT DATE_TRUNC('month', ABNStatusFromDate) AS month, COUNT(*) as total FROM my_db.active_private_company GROUP BY month ORDER BY month;").show()

# # extract data
# # 月
# df=con.sql("SELECT state, EXTRACT(MONTH FROM ABNStatusFromDate) AS month, COUNT(*) as total FROM my_db.active_private_company GROUP BY state,month ORDER BY state,month;").fetchdf()
# print(df.head(20))
# # 年-月
# # DATE_TRUNC('month', ABNStatusFromDate) AS month

# # write data to csv file
# df.to_csv('bymonth.csv', index=False)

# con.close()
