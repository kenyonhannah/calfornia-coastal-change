# import statements
import calendar
import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

'''
Program Process: analyzes shoreline position data by resampling, interpolating, 
detrending, and generating basic statistics on data 
Input/Parameters: filepath to raw CoastSeg transect data 
Output: 4 unique CSV's: amplitude, 
month of maximum shoreline position for that transect, 
month of minimum shoreline position for that transect, 
monthly mean detrended shoreline positions for each transect 
Dependencies: pandas, calendar, statsmodels, matplotlib
'''

def main():
    # get filepath of raw data csv from user
    filepath = input('CoastSeg Raw Transect Data Filepath: ')
    beach_id = input('Name or abbreviation of the beach for filename: ')

    # save to dataframe
    # pandas function: read_csv()
    df_original = pd.read_csv(filepath)

    # prep data
    # custom function: prepare_data()
    df_prepped = prepare_data(df_original)

    # add dates if missing months
    # custom function: add_missing_months()
    df = add_missing_months(df_prepped)

    if 'Unnamed: 0' in df.columns:
        # remove unnecessary column
        df = df.drop(columns='Unnamed: 0')

    # interpolate
    # custom function: interpolate_data()
    df = interpolate_data(df)

    # reclassify to monthly
    # custom function: resample()
    df_reclassed = resample(df)

    # run stl
    # custom function: stl()
    trend_data = stl(df_reclassed)

    # detrend
    # custom function: detrend()
    detrended_data = detrend(df_reclassed, trend_data)

    # mean monthly detrended data
    # custom function: monthly_mean()
    monthly_mean_data = monthly_mean(detrended_data)

    # save monthly means to ArcGIS Pro compatible format
    # custom function: reformat_monthly_mean()
    reformat_monthly_mean(monthly_mean_data, beach_id)

    # amplitudes of each transect
    # custom function: amplitude()
    amplitude(monthly_mean_data, beach_id)

    # get month with maximum value for each transect
    # custom function: minimum_month()
    minimum_month(detrended_data, beach_id)

    # get month with minimum value for each transect
    # custom function: maximum_month()
    maximum_month(detrended_data, beach_id)

    # ask user if they want any plots of data
    plot = input('Would you like a plot of a specific transects data? (y/n): ')

    # if yes
    if plot == 'y':
        # generate plot
        # custom function: plot_transect_data()
        plot_transect_data(df_prepped, df_reclassed, trend_data, detrended_data, beach_id)

    # confirm status
    print('Analysis is complete')
    print('CSV files of output have been created')


# Supporting Functions:
'''
Function Name: add_missing_months 
Process: finds any missing months in the timestamp column and adds a row for
that month into all transects where the value in the transect column is NaN.
All transects share the timestamp column, so a missing date will be universal
for all transects.
Input/Parameters: dataframe of raw data
Output: N/A
Return: dataframe of raw data where there is a timestamp value for every month
of every year
Dependencies: pandas, numpy
'''


def add_missing_months(df):
    # set intial values
    year = 1984
    month = 1

    # while not at the end of the dates
    while year != 2022:
        # create date
        # if month is less than 10
        if month < 10:
            # add a zero to the month
            date = str(year) + '-0' + str(month) + '-01'
        else:
            # dont add a zero
            date = str(year) + '-' + str(month) + '-01'

        if not ((df['timestamp'] == date).any()):
            # define row
            new_row = {'timestamp': date}

            # insert new row (loc) at the end of the df (len(df))
            df.loc[len(df.index)] = new_row

            # set new row timestamp value to datetime, when first inserted it is a string
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # set new date
            # if not the end of the year
        if month != 12:
            month += 1
            # else end of the year
        else:
            year += 1
            month = 1

    # sort df by timestamp values
    df = df.sort_values(by='timestamp')

    # reset the index so the sorted data has a sorted index
    df = df.reset_index(drop=True)

    # return df
    return df


'''
Function Name: amplitude 
Process: calculates amplitude from monthly mean data 
Input/Parameters: df of monthly mean data 
Output: csv of amplitude data for each month 
Return: N/A
Dependencies: pandas 
'''


def amplitude(df, beachID):

    # initialize results df
    df_amplitude = pd.DataFrame(columns=['transectID', 'amplitude'])

    # for each transect in the df, skips timestamp column
    for col in df.columns:
        # get max position
        max_position = df[col].max()

        # get min position
        min_position = df[col].min()

        # calculate amplitude
        amplitude = (max_position - min_position) / 2

        df_amplitude = pd.concat([df_amplitude, pd.DataFrame(
            {'transectID': [col], 'amplitude': [amplitude]})],
                                 ignore_index=True)

    # save df to a csv
    df_amplitude.to_csv('results/amplitude_{}.csv'.format(beachID))


'''
Function Name: detrend 
Process: subtracts trend from original data to get detrended data 
Input/Parameters: original data(df), trend_data(df)
Output: N/A
Return: df of detrended data 
Dependencies: pandas 
'''


def detrend(original_data, trend_data):
    # initialize detrended data dictionary
    detrended_data_dict = {}

    # add timestamp column
    detrended_data_dict['timestamp'] = original_data['timestamp']

    # reset indices to 0 for calculation purposes
    original_data = original_data.reset_index(drop=True)
    trend_data = trend_data.reset_index(drop=True)

    # for each column in the dataframes
    for col in original_data.columns[1:]:
        # calculate detrended data
        detrended_data = original_data[col] - trend_data[col]

        # save data to dict
        detrended_data_dict[col] = detrended_data

    # Concatenate all detrended data into a new DataFrame
    df_detrended = pd.concat(detrended_data_dict.values(), axis=1,
                             keys=detrended_data_dict.keys())


    # return
    return df_detrended


'''
Function Name: interpolate_data
Process: interpolates data
Input/Parameters: df of data with unnamed column dropped 
Output: N/A
Return: df of interpolated data
Dependencies: pandas 
'''


def interpolate_data(df):

    # prep data for interpolation
    # if first row contains NaN's
    if df.iloc[0].isna().any():

        # for each column in the dataframe
        for col in df.columns:

            # if first value in the column is NaN
            if pd.isna(df[col].iloc[0]):

                # find the closest non-NaN value from the following rows
                next_valid_index = df[col].iloc[1:].first_valid_index()

                # get the value from the next valid index
                if next_valid_index is not None:
                    replacement_value = df[col][next_valid_index]
                    df.at[0, col] = replacement_value

    # pandas function: interpolate()
    df = df.interpolate(method='linear')

    # return
    return df


'''
Function Name: minimum_month
Process: grabs month of minimum value for each transect
Input/Parameters: df of monthly mean data 
Output: csv file of minimum months
Return: N/A
Dependencies: pandas, calendar 
'''


def maximum_month(df, beachID):
    # initialize results dataframe
    df_maximum_month = pd.DataFrame(
        columns=['transectID', 'maximum_month_number', 'maximum_month_name'])

    # for each column in the dataframe, skips timestamp column
    for col in df.columns[1:]:
        # find the row of the minimum values and save row to dataframe
        max_value_row = df[df[col] == df[col].max()]

        # grab month that value occurs
        # cast to string, slice string to grab only month value
        max_month = str(max_value_row['timestamp'].iloc[0])[5:7]

        # set month name
        # cast month to integer so calendar function can operate
        max_month_name = calendar.month_name[int(max_month)]

        # store month to df
        df_maximum_month = pd.concat([df_maximum_month, pd.DataFrame({
            'transectID': [col], 'maximum_month_number': [max_month],
            'maximum_month_name': [max_month_name]})], ignore_index=True)

    # save df to csv
    df_maximum_month.to_csv('results/maximum_month_{}.csv'.format(beachID))


'''
Function Name: minimum_month
Process: grabs month of minimum value for each transect
Input/Parameters: df of monthly mean data 
Output: csv file of minimum months
Return: N/A
Dependencies: pandas, calendar 
'''


def minimum_month(df, beachID):
    # initialize results dataframe
    df_minimum_month = pd.DataFrame(
        columns=['transectID', 'minimum_month_number', 'minimum_month_name'])

    # for each column in the dataframe, skips timestamp column
    for col in df.columns[1:]:
        # find the row of the minimum values and save row to dataframe
        min_value_row = df[df[col] == df[col].min()]

        # grab month that value occurs
        # cast to string, slice string to grab only month value
        min_date = str(min_value_row['timestamp'].iloc[0])
        min_month = (min_date)[5:7]

        # set month name
        # cast month to integer so calendar function can operate
        min_month_name = calendar.month_name[int(min_month)]

        # store month to df
        df_minimum_month = pd.concat([df_minimum_month, pd.DataFrame({
            'transectID': [col], 'minimum_month_number': [min_month],
            'minimum_month_name': [min_month_name]})], ignore_index=True)

    # save df to csv
    df_minimum_month.to_csv('results/minimum_month_{}.csv'.format(beachID))


'''
Function Name: monthly_mean
Process: calculates monthly mean of all year data 
Input/Parameters: df of detrended data
Output: N/A
Return: df of monthly means 
Dependencies: pandas 
'''


def monthly_mean(df):
    # initialize dictionary of results
    monthly_mean_dict = {}

    # for each transect in the csv
    for col in df.columns[1:]:
        # group by month and calculate the mean for each month
        monthlyMeans = df.groupby(df['timestamp'].dt.month)[col].mean()

        # save transect means with new column name 'transectID_mean'
        monthly_mean_dict[col] = monthlyMeans

    # concatenate all trend data into new df
    df_monthly_means = pd.concat(monthly_mean_dict.values(), axis=1, keys=
    monthly_mean_dict.keys())

    # return
    return df_monthly_means


'''
Function Name: plot_transect_data
Process: plots raw data, trend data, and detrended data for specified transect
Input/Parameters: df of raw data, df of trend data, df of detrened data 
Output: multipanel plot of data
Return: N/A
Dependencies: pandas, matplotlib
'''


def plot_transect_data(df_prepped, df_reclassed, df_trend, df_detrended, beachID):

    # get transect from user
    transect_number = input('Which transect number would you like to plot?: ')
    transect = "region_29_" + transect_number

    # define y's
    y_original = df_prepped[transect]

    y_reclassed = df_reclassed[transect]

    y_trend = df_trend[transect]

    y_detrended = df_detrended[transect]

    # define x for plotting
    x_data_original = df_prepped['timestamp']


    x_data_reclassed = df_reclassed['timestamp']


    # plot
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 8))

    axes[0].plot(x_data_original, y_original, label='Raw Data')
    axes[0].set_title('Shoreline Position at Transect #{} Over Time'
                      .format(transect_number))
    axes[0].legend()

    axes[1].plot(x_data_reclassed, y_reclassed, label='Interpolated Reclassified'
                                                      ' Data')
    axes[1].set_title('Interpolated & Reclassified Shoreline Position at '
                      'Transect #{} Over Time'
                      .format(transect_number))
    axes[1].legend()

    axes[2].plot(x_data_reclassed, y_trend, label='Trend Data')
    axes[2].set_title('Trend at Transect #{} Over Time'.format(transect_number))
    axes[2].legend()

    axes[3].plot(x_data_reclassed, y_detrended, label='Detrended Data')
    axes[3].set_title('Detrended Shoreline Position at Transect #{} Over Time'
                      .format(transect_number))
    axes[3].legend()

    plt.tight_layout()
    plt.show()


'''
Function Name: prepare_data 
Process: removes data before 2000 and ensures timestamps are dtype datetime
Input/Parameters: dataframe of raw data
Output: N/A
Return: dataframe of prepped data
Dependencies: pandas
'''


def prepare_data(df):
    # remove seconds, minutes, days
    df['timestamp'] = df['timestamp'].str.slice(stop=7)

    # convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # return df
    return df

'''
Function Name: resample
Process: resample to monthly value consisting of mean for all data from that month 
Input/Parameters: df of interpolated data
Output: N/A
Return: df of resampled data 
Dependencies: pandas 
'''
def resample(df):

    # Set 'timestamp' as the index of the DataFrame
    df.set_index('timestamp', inplace=True)

    # Resample data by month and calculate the mean
    df_reclassed = df.resample('M').mean()

    # Reset index to turn 'timestamp' back into a regular column
    df_reclassed.reset_index(inplace=True)

    # return
    return df_reclassed


'''
Function Name: reformat_monthly_mean
Process: reformat monthly mean df to be computable with ArcGIS Pro field joins 
Input/Parameters: df of monthly mean data 
Output: csv of monthly mean data reformatted
Return: N/A
Dependencies: pandas 
'''


def reformat_monthly_mean(df, beachID):
    # save monthly mean data to ArcGIS Pro compatible format
    df = df.transpose()

    # save to csv
    df.to_csv('results/monthly_mean_reformatted_{}.csv'.format(beachID),
              index_label='transectID')


'''
Function Name: stl
Process: runs statsmodels stl tool on reclassified data
Input/Parameters: dataframe of reclassified data 
Output: N/A
Return: dataframe of trend data 
Dependencies: pandas, statsmodels stl 
'''


def stl(df):
    # initialize dictionary to hold trend results
    trend_data_dict = {}

    # for each column in the dataframe
    for col in df.columns[1:]:
        # Convert the column to a series
        series = pd.Series(df[col].values, index=df['timestamp'].copy())

        # run stl
        stl = STL(series, period=12, trend=13, seasonal=13, robust=True,
                  seasonal_deg=1, trend_deg=1, low_pass_deg=1)
        result = stl.fit()

        # store trend data in dictionary
        trend_data_dict[col] = result.trend

    # concatenate all trend data into a new DataFrame
    df_trend = pd.concat(trend_data_dict.values(), axis=1,
                         keys=trend_data_dict.keys())

    # return
    return df_trend


# call main
main()
