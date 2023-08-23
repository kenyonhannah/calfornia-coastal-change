# import statement
import pandas as pd
import matplotlib
import numpy as np
import random
import math
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def main():
    # save csv into a dataframe
    filepath = r'C:\Users\kenyo\shorelineAnalysis\coast_sat_data\dataset_california_2022_07_v5b\'
    columns_to_select = ['timestamp', 'usa_CA_0003-0004']
    df = no_missing_df[columns_to_select].copy()
    print(len(df))
    df.to_csv('raw_data_0003-0004.csv')
    df_nan = add_nan(df)
    print(len(df_nan))

    # interpolation
    df_nan = linear_interpolation(df_nan)
    df_nan.to_csv('interpolated.csv')
    print(len(df_nan))

    # resampling
    df_interpolated = resample_to_monthly(r'C:\Users\kenyo\shorelineAnalysis\interpolated.csv')
    df_interpolated.to_csv('interpolated_resampled.csv')
    print(len(df_interpolated))
    df_raw = resample_to_monthly(r'C:\Users\kenyo\shorelineAnalysis\raw_data_0003-0004.csv')
    df_raw.to_csv('raw_resampled.csv')
    print(len(df_raw))

    # rmse
    y_actual = df_raw['usa_CA_0003-0004']
    y_interpolated = df_interpolated['usa_CA_0003-0004']
    print(calculate_rmse(y_actual, y_interpolated))



    # count amount of NaN in each column
    # for col in df.columns[1:]:
    #     NaN = df[col].isna().sum()
    #     print(NaN)
    # df = add_missing_values(filepath)
    # spline = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\data_investigation\spline_interpolated.csv')
    # polynomial = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\data_investigation\polynomial_interpolated.csv')


    # linear = linear_interpolation(df)
    # # spline = spline_interpolation(df)
    # # polynomial = polynomial_interpolation(df)
    # rmse(no_missing_df, linear, spline, polynomial)

'''
Function Name: resample_to_monthly
Process: for each year in the data set, the monthly mean shoreline position is calculated
Input/Parameters: dataframe of timeseries (single transect)
Output: dataframe of timeseries reclassed to monthly increments 
based on the mean of each month 
Return: dataframe of mean shoreline position for each month for each year 
Dependencies: pandas functions 
'''
def resample_to_monthly(csv_filepath):
    # save csv to dataframe
    df = pd.read_csv(csv_filepath)

    # grab test transect
    transect = df[['timestamp', 'usa_CA_0003-0004']].copy()

    # remove row 268 as it is NaN
    # df = transect.drop(labels=[268], axis=0)

    # remove seconds, minutes, days
    df['timestamp'] = df['timestamp'].str.slice(stop=7)

    # set timestamp values to datetime datatype
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # create new df where shoreline position value is the mean of all values taken that month
    newdf = df.groupby(['timestamp'], as_index=False).mean()

    return newdf


'''
Function Name: add_nan
Process: 
Input/Parameters: dataframe of resampled time series 
Output: csv of dataframe of resampled time series with random missing rows 
Return: 
Dependencies: pandas functions 
'''
def add_nan(df):

    # initalize random seed
    np.random.seed()

    # set amount to remove
    remove_n = 31

    # drop
    drop_indices = np.random.choice(df.index, remove_n, replace=False)

    for row in range(len(drop_indices)):
        df.at[drop_indices[row], 'usa_CA_0003-0004'] = np.nan

    # save to new
    # df_subset = df.drop(drop_indices)

    return df


'''
Function Name: add_missing_values 
Process: from 
Input/Parameters: filepath to csv of resampled data where there are missing 
Output: csv of resampled data, at regular increments, where missing values have been filled in with interpolated values 
Return: 
Dependencies: pandas functions 
'''
def add_missing_values(csv_filepath):
    # save csv to dataframe
    df = pd.read_csv(csv_filepath)

    # set timestamp values to datetime datatype
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # HOW TO INSERT A NEW ROW
    # # define new row: { column : value, row: value}
    # new_row = {'timestamp': '1984-01', 'usa_CA_0003-0004': 207.46}
    #
    # # insert new row (loc) at the end of the df (len(df))
    # newdf.loc[len(newdf.index)] = new_row
    #
    # # set new row timestamp value to datetime, when first inserted it is a string
    # newdf['timestamp'] = pd.to_datetime(newdf['timestamp'])
    #
    # # sort df by timestamp values
    # newdf = newdf.sort_values(by='timestamp')
    #
    # # reset the index so the sorted data has a sorted index
    # newdf = newdf.reset_index(drop=True)

    # reinsert missing timestamps with no value
    # set start date
    year = 2009
    month = 1

    # while not at the end of the dates
    while year != 2019:
        # create date value
        # if month is less than 10
        if month < 10:
            # add a zero to the month
            date = str(year) + '-0' + str(month) + '-01'
        else:
            # dont add a zero
            date = str(year) + '-' + str(month) + '-01'

        # if date is not in timestamp column
        if not ((df['timestamp'] == date).any()):
            # define row
            new_row = {'timestamp': date, 'usa_CA_0003-0004': np.nan}

            # insert new row (loc) at the end of the df (len(df))
            df.loc[len(df.index)] = new_row

            # set new row timestamp value to datetime, when first inserted it is a string
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        # set new date
        # if not the end of the year
        if month != 12:
            month += 1
        # else its
        elif month == 12:
            year += 1
            if year == 2011:
                year = 2012
            elif year == 2016:
                year = 2017
            month = 1

    # sort df by timestamp values
    df = df.sort_values(by='timestamp')

    # reset the index so the sorted data has a sorted index
    df = df.reset_index(drop=True)

    df.to_csv('missing_data_with_NaNs.csv')

    return df

def linear_interpolation(df):

    # linear interpolation
    df = df.interpolate(method='linear', limit_direction='forward', limit_area='inside')

    return df

# def spline_interpolation(df):
#
#     # linear interpolation
#     df = df.interpolate(method='spline', order=1)
#
#     return df
#
# def polynomial_interpolation(df):
#
#     # linear interpolation
#     df = df.interpolate(method='polynomial', order=1)
#
#     return df


def calculate_rmse(actual_values, predicted_values):
    # Convert inputs to numpy arrays to ensure they are compatible
    actual_values = np.array(actual_values)
    predicted_values = np.array(predicted_values)

    # Calculate squared differences
    squared_diff = (predicted_values - actual_values) ** 2

    # Calculate mean of squared differences
    mean_squared_diff = squared_diff.mean()

    # Calculate RMSE by taking the square root of mean_squared_diff
    rmse = np.sqrt(mean_squared_diff)

    return rmse


def rmse(df, df_linear, df_spline, df_polynomial, rmse_polynomial=None):

    # define y's
    y_actual = df['usa_CA_0197-0007']

    y_linear = df_linear['usa_CA_0197-0007']

    y_spline = df_spline['usa_CA_0197-0007']

    y_polynomial = df_polynomial['usa_CA_0197-0007']

    # define x for plotting
    xdata = df['timestamp']

    # get RMSE
    rmse_true = calculate_rmse(y_actual, y_actual)
    rmse_linear = calculate_rmse(y_actual, y_linear)
    rmse_spline = calculate_rmse(y_actual, y_spline)
    rmse_polynomial = calculate_rmse(y_actual, y_polynomial)

    # show RMSE
    print(rmse_true)
    print('RMSE for Linear Interpolated Data: ', rmse_linear)
    print('RMSE for Spline Interpolated Data: ',rmse_spline)
    print('RMSE for Polynomial Interpolated Data: ',rmse_polynomial)

    # plot
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))

    axes[0].plot(xdata, y_actual, label='Actual Data')
    axes[0].plot(xdata, y_linear, label='Linear Interpolated Data')
    axes[0].set_title('Actual v. Linear')
    axes[0].legend()

    axes[1].plot(xdata, y_actual, label='Actual Data')
    axes[1].plot(xdata, y_spline, label='Spline Interpolated Data')
    axes[1].set_title('Actual v. Spline')
    axes[1].legend()

    axes[2].plot(xdata, y_actual, label='Actual Data')
    axes[2].plot(xdata, y_polynomial, label='Polynomial Interpolated Data')
    axes[2].set_title('Actual v. Polynomial')
    axes[2].legend()

    plt.tight_layout()
    plt.show()

    # plt.plot(xdata, y_actual, label = 'actual')
    # plt.plot(xdata, y_linear, label = 'linear interpolated')
    # plt.plot(xdata, y_spline, label='spline interpolated')
    # plt.plot(xdata, y_polynomial, label='polynomial interpolated')
    # plt.legend()
    # plt.show()

main()
