# import statements
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import STL

def dummy_data_stl():
    # sample time series parameters
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    frequency = 'M'
    amp = 5
    freq_sine = 2 * np.pi / 12
    slope = 0.2
    intercept = 2

    # create time series date range
    date_range = pd.date_range(start=start_date, end=end_date, freq=frequency)

    # generate sine wave
    sine = amp * np.sin(freq_sine * np.arange(len(date_range)))

    # generate linear trend
    linear_trend = slope * np.arange(len(date_range)) + intercept

    # combine sine and linear
    combined_data = linear_trend + sine

    # save to dataframe
    data = {'Date' : date_range, 'Data': combined_data}
    df_original = pd.DataFrame(data)

    # save to series
    data_series = pd.Series(df_original['Data'])

    # get statistics
    data_series.describe()

    # run stl
    stl = STL(data_series, period=12, trend=13, seasonal=13, trend_deg=1)
    results = stl.fit()

    # save trend data
    trend_data = {'Date':date_range, 'Trend': results.trend}
    df_trend = pd.DataFrame(trend_data)

    # detrend data
    detrended_data = {'Date':date_range, 'Detrend': (df_original['Data'] - df_trend['Trend'])}
    df_detrended = pd.DataFrame(detrended_data)

    # plot
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))

    axes[0].plot(df_original['Date'], df_original['Data'], label='Original Data')
    axes[0].set_title('Original Data')
    axes[0].legend()

    axes[1].plot(df_trend['Date'], df_trend['Trend'], label='Trend')
    axes[1].set_title('Trend from STL')
    axes[1].legend()

    axes[2].plot(df_detrended['Date'], df_detrended['Detrend'], label='Detrended Data')
    axes[2].set_title('Detrended Data')
    axes[2].legend()

    plt.tight_layout()
    plt.show()

def real_data_stl():

    # save csv to df
    df = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\reclassed_0026_0010.csv')

    # merge transect data
    transect = 'usa_CA_0026-0010'
    endYear = 2020
    startYear = 2014

    # convert date column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # filter data to only include user specified years
    df = df[(df['timestamp'].dt.year <= endYear) & (df['timestamp'].dt.year >= startYear)]

    # extract transect data into a series
    transectSeries = pd.Series(df[transect].values, index=df['timestamp'])

    # get statistics
    transectSeries.describe()

    # perform SLT analysis
        # seasonal must be ODD so that the window of estimation
        # can be centered around each point
    stl = STL(transectSeries, period=12,trend = 13, seasonal = 13, robust=True, seasonal_deg=1, trend_deg=1)
    results = stl.fit()

    # set date range
    date_range = df['timestamp']

    # save trend data
    trend_data = {'Trend': results.trend}
    df_trend = pd.DataFrame(trend_data)

    # reset indices for detrend calculation
    df_trend = df_trend.reset_index(drop=True)
    df = df.reset_index(drop=True)

    # detrend data
        # calculate detrended data
    detrended_data = {'Detrend': (df[transect] - df_trend['Trend'])}
    df_detrended = pd.DataFrame(detrended_data)

    # plot
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))

    axes[0].plot(df['timestamp'], df[transect],
                 label='Original Data')
    axes[0].set_title('Original Data')
    axes[0].legend()

    axes[1].plot(date_range, trend_data['Trend'], label='Trend')
    axes[1].set_title('Trend from STL')
    axes[1].legend()

    axes[2].plot(date_range, df_detrended['Detrend'],
                 label='Detrended Data')
    axes[2].set_title('Detrended Data')
    axes[2].legend()

    plt.tight_layout()
    plt.show()

real_data_stl()
