# import statements
import pandas as pd
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

    # save csv to dataframe
    df = pd.read_csv(csvFilePath)

    # convert timestamp column to datetime format
    df['month'] = pd.to_datetime(df['timestamp'], format='%m')

    # plot
    monthformat = mdates.DateFormatter('%b')
    plt.gca().xaxis.set_major_formatter(monthformat)
    plt.scatter( df['month'], df[transect] )
    plt.xlabel('Month')
    plt.ylabel('Mean Shoreline Position')
    title = f"Santa Clara Mean {transect} Shoreline Position over Time"
    plt.title(title)
    plt.show()
