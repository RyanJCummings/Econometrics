import pandas as pd
import numpy as np


def normalize_revenue_data(revenue_path):
    raw_data = pd.read_csv(revenue_path, sep=',')
#    print(raw_data.to_string)


def calculate_quartly_cpi(cpi_path):
    """averages the monthly CPILEGNS using arithmetic mean

    Parameters
    ----------
    cpi_path : str
    path to CPI data csv file

    Returns
    -------
    quarterly_cpi : Pandas DataFrame
        new dataframe that reorganizes the cpi from monthly to quarterly
    """

    start_date = '2009-03-30'
    end_date = '2023-10-01'

    # read in csv file and process into dataframe
    monthly_cpi = pd.read_csv(cpi_path)
    monthly_cpi = monthly_cpi.set_index('DATE')

    # remove unneeded data by date range
    # the boolean mask is a good idea from Gemini (google's chatbot)
    mask = (monthly_cpi['DATE'] >= start_date & monthly_cpi['DATE'] <= end_date)
    filtered_cpi = monthly_cpi[mask]

    # Dates are formatted as strings and must be converted to
    # datetime objects so pandas can work with them
    filtered_cpi.index = pd.to_datetime(monthly_cpi.index)

    # resample() converts monthly to quarterly data using arithmetic mean
    quarterly_cpi = monthly_cpi.resample('Q')['CPILEGNS'].mean()

    # reset_index makes dataframe easy for pandas to mutate
    quarterly_cpi = quarterly_cpi.reset_index()

    print("quarterly_cpi")
    print(quarterly_cpi.to_string)
    quarterly_cpi.to_csv('quarterly_cpi.csv')
    return quarterly_cpi


def main():
    cpi_path = "CPILEGNS.csv"
    revenue_path = "raw_data.csv"

    quarterly_cpi = calculate_quartly_cpi(cpi_path)
    normalized_data = normalize_revenue_data(revenue_path)


main()
