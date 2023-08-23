# import statements
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():

    # get user input
    filePath = r'C:\Users\kenyo\shorelineAnalysis\SantaClara\coastSat_data\usa_CA_0088_time_series_after2000.csv'

    # find means
    # calcSeasonMonthlyMeans( filePath )

    filePath = r'C:\Users\kenyo\shorelineAnalysis\seasonal_monthly_means_.csv'
    transectID = input("Transect ID: ")

    # graph means
    graphStats( filePath, transectID  )

    # confirmation message
    print("csv file created")

    # ask user to run again
    # rerun = input( "Would you like to analyze more data? (y/n): ")

    # while (rerun == 'y'):
        # get user input
        # filePath = input('Filepath: ')

        # find means
        # calcSeasonMonthlyMeans(filePath)

        # confirmation message
        # print("csv file created")

        # ask user to run again
        # rerun = input("Would you like to analyze more data? (y/n): ")


def calcSeasonMonthlyMeans(csvFilePath):

    # save csvs into dataframes
    df = pd.read_csv(csvFilePath)

    # beachID = csvFilePath[56:60]

    # convert date column to datetime format
    df['dates'] = pd.to_datetime(df['dates'])

    # initalize dataframe to save to
    meansDF = pd.DataFrame()

    # for each transect in the csv
    for col in df.columns:
        if (col != 'dates'):
            # Group by month and calculate the mean for each month
            monthlyMeans = df.groupby(df['dates'].dt.month)[col].mean()

            meansDF[col + '_mean'] = monthlyMeans

    # save dataframe to a csv
    meansDF.to_csv("seasonal_monthly_means_.csv" )

def graphStats( csvFilePath, transectEnd ):

    # save csv to dataframe
    df = pd.read_csv(csvFilePath)

    transect_base = 'usa_CA_0088-'
    transect = transect_base + transectEnd +'_mean'

    # convert timestamp column to datetime format

    df['dates'] = pd.to_datetime(df['dates'], format='%m')

    print(df)

    # plot
    monthformat = mdates.DateFormatter('%b')
    plt.gca().xaxis.set_major_formatter(monthformat)
    plt.scatter( df['dates'], df[transect] )
    plt.xlabel('Month')
    plt.ylabel('Mean Shoreline Position')
    title = f"Santa Clara Mean Shoreline Position over Time: {transect}"
    plt.title(title)
    plt.show()

main()