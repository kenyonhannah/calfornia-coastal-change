# import libraries
import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import matplotlib.pyplot as plt

# main function
def main():
    # initalize variables
    transect = 'usa_CA_0088-0000'

        # import csv into dataframes
    santaClaraShorelines = pd.read_csv(r'C:\Users\kenyo\Desktop\USGS\SampleData\SantaClaraEvent\usa_CA_0088_time_series.csv')
    saltCreekShorelines = pd.read_csv(r'C:\Users\kenyo\Desktop\USGS\SampleData\SaltCreekSeasonal\usa_CA_0026_time_series.csv')

    # processing
        # generate time series plots
            # Convert 'Date' column to datetime type
    santaClaraShorelines['Date'] = pd.to_datetime(santaClaraShorelines['dates'])

        # Set 'Date' as the index of the DataFrame
    santaClaraShorelines.set_index('Date', inplace=True)

    # Generate plot
    plt.plot(santaClaraShorelines.index, santaClaraShorelines[transect])
    plt.xlabel('Date')
    plt.ylabel('Shoreline Location')
    plt.title('Time Series Plot')
    plt.show()

main()
