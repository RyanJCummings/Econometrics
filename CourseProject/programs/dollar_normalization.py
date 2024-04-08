import pandas as pd
import numpy as np


def derive_quarterly_cpi(cpi_path):

    # Read csv file into pandas dataframe
    monthly_cpi = pd.read_csv(cpi_path)

    # Filter by date range
    monthly_cpi['DATE'] = pd.to_datetime(monthly_cpi['DATE'])
    monthly_cpi.set_index('DATE')
    monthly_cpi = monthly_cpi.loc[(monthly_cpi['DATE'] >= '2009-1-1') & (monthly_cpi['DATE'] <= '2023-9-30')]
    monthly_cpi.reset_index(drop=True, inplace=True)

    # Transform to quarterly CPI using arithmetic mean
    quarterly_cpi = monthly_cpi.set_index('DATE').resample('Q').mean().round(1)

    return quarterly_cpi


def normalize_revenue_data(revenue_path, cpi):
    # read revenue data csv and format as pandas dataframe
    nominal_data = pd.read_csv(revenue_path)
    # print(nominal_data)

    # Do some formatting to make it easier to work with
    nominal_data = nominal_data.rename(columns={"AWR Date": "awr_date",
                                 "AWR Quarterly Revenue (Millions USD)": "awr_nom",
                                 "RRGB Date": "rrgb_date",
                                 "RRGB Quarterly Revenue (Millions USD)": "rrbg_nom"})
    return calculate_real_value(nominal_data, cpi)


def calculate_real_value(data, cpi):
    data['cpi'] = cpi['CPILEGNS'].values

    data['awr_nom'] = data['awr_nom'].str.replace('$', '')
    data['awr_nom'] = pd.to_numeric(data['awr_nom'])
    awr_real = data.eval('awr_nom / cpi * 100').round(1)
    data.insert(loc=2, column='awr_real', value=awr_real)

    data['rrbg_nom'] = data['rrbg_nom'].str.replace('$', '')
    data['rrbg_nom'] = pd.to_numeric(data['rrbg_nom'])
    awr_real = data.eval('rrbg_nom / cpi * 100').round(1)
    data.insert(loc=5, column='rrbg_real', value=awr_real)

    return data


def main():
    cpi_path = "CPILEGNS.csv"
    revenue_path = "raw_data.csv"

    quarterly_cpi = derive_quarterly_cpi(cpi_path)
    real_dollar_data = normalize_revenue_data(revenue_path, quarterly_cpi)
    real_dollar_data.to_csv('groomed_data.csv', index=False)
    print(real_dollar_data)


main()
