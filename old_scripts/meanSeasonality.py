# import statements
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():

    # get user input
    # filePath = r'C:\Users\kenyo\shorelineAnalysis\monthly_means_.csv'
    filePath = r'/data_investigation/missing_data/missing_data_monthly_means.csv'

    # find means
    # calcSeasonMonthlyMeans( filePath )

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

    # INPUT: data to turn into monthly means

    # save csvs into dataframes
    df = pd.read_csv(csvFilePath)

    # beachID = csvFilePath[56:60]

    # convert date column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # initalize dataframe to save to
    meansDF = pd.DataFrame()

    # for each transect in the csv
    for col in df.columns:
        if (col != 'timestamp'):
            # Group by month and calculate the mean for each month
            monthlyMeans = df.groupby(df['timestamp'].dt.month)[col].mean()

            meansDF[col + '_mean'] = monthlyMeans

    # save dataframe to a csv
    meansDF.to_csv("monthly_means_.csv" )

def graphStats( csvFilePath, transectEnd ):

    # INPUT: monthly mean values
    # OUTPUT: plot

    # save csv to dataframe
    df = pd.read_csv(csvFilePath)

    transect_base = 'usa_CA_0003-'
    transect = transect_base + transectEnd + '_mean'

    # convert timestamp column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m')

    print(df)

    # plot
    monthformat = mdates.DateFormatter('%b')
    plt.gca().xaxis.set_major_formatter(monthformat)
    plt.scatter( df['timestamp'], df[transect] )
    plt.xlabel('Month')
    plt.ylabel('Mean Shoreline Position')
    title = f"Mean Shoreline Position over Time: {transect}"
    plt.title(title)
    plt.show()


main()
