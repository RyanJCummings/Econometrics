import pandas as pd
# import numpy as np


def normalize_revenue_data(revenue_path):
    raw_data = pd.read_csv(revenue_path, sep=',')
    print(raw_data.to_string)


def calculate_quartly_cpi(cpi_path):
    """averages the monthly CPILEGNS using arithmetic mean"""
    monthly_cpi = pd.read_csv(cpi_path)
    # print(monthly_cpi.to_string)



def main():
    cpi_path = "CPILEGNS.csv"
    revenue_path = "raw_data.csv"

    quarterly_cpi = calculate_quartly_cpi(cpi_path)
    normalized_data = normalize_revenue_data(revenue_path)


main()
