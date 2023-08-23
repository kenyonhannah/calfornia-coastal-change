# import libraries
import matplotlib
import pandas as pd
import seaborn as sns
from statsmodels.tsa.seasonal import STL
from statsmodels.datasets import elec_equip as ds
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##### CAN ONLY BE RUN ON REGULARLY INTERVALED DATA WITH NO NaN #####
# INPUT: reclassified coastSat data
# OUTPUT: csv of trend data calculated from Statsmodels STL

def main():

    # get user input
    filePath = input("Filepath: ")

    # run STL analysis on given file
    STLanalysis( filePath )

    # confirmation message
    print("CSV file has been created")

    # ask user if they would like to repeat
    repeat = input("Would you like to analyze more data? (y/n): ")

    # while user wants to repeat
    while (repeat == 'y'):

        # get user input
        filePath = input("Filepath: ")

        # run STL analysis on file
        STLanalysis( filePath )

        # ask user if they would like to repeat
        repeat = input("Would you like to analyze more data? (y/n): ")

# function that runs the STL analysis on given file then saves results to a csv file
def STLanalysis( csvFilePath ):

    # load transect data into dataframe
    df = pd.read_csv(csvFilePath)

    beachID = csvFilePath[83:87]

    # remove hours, seconds, minutes from 'dates' column
    df['timestamp'] = df['timestamp'].str.slice(stop=10)

    # convert dates to datetime
    df['timestamp'] = pd.to_datetime( df['timestamp'] )


    # initalize dataframe for seasonality data to be stored
    resultsDF = pd.DataFrame()

    # for each transect in the dataframe
    for col in df.columns:

        # convert to a series
        series = pd.Series(df[col].values, index=df['timestamp'].copy())

        # get stats
        series.describe()

        # run STL
        stl = STL(series, seasonal= 13, robust = True, seasonal_deg = 1, trend_deg = 1, low_pass_deg = 1 )
        result = stl.fit()

        # store STL seasonality to a new dataframe
        if ( col != 'timestamp' ):
            resultsDF[col] = result.trend

    # save dataframe to a csv
    resultsDF.to_csv("stl_trend_results_{}.csv".format(beachID) )

main()