# import libraries
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
from statsmodels.datasets import elec_equip as ds

##### CAN ONLY BE RUN ON REGULARLY INTERVALED DATA WITH NO NaN #####

def main():

    # get user input
    dataSet = input("Santa Clara or Salt Creek dataset?: ")
    transectNumber = input("Transect number [0000 - 0012] : ")
    userStartYear = input("What year would you like to start at? ")
    userEndYear = input("What year would you like to end at? ")

    # datatype transfers
    startYear = int(userStartYear)
    endYear = int(userEndYear)

    STLanalysis(transectNumber, dataSet, startYear, endYear)
    repeat = input("Would you like to analyze more data? (y/n): ")

    while (repeat == 'y'):
        # get user input
        dataSet = input("Santa Clara or Salt Creek dataset?: ")
        transectNumber = input("Transect number [0000 - 0012] : ")
        userStartYear = input("What year would you like to start at? ")
        userEndYear = input("What year would you like to end at? ")

        # datatype transfers
        startYear = int(userStartYear)
        endYear = int(userEndYear)

        STLanalysis(transectNumber, dataSet, startYear, endYear)
        repeat = input("Would you like to analyze more data? (y/n): ")


def STLanalysis(transectNumber, dataSet, startYear, endYear):

    # function to register converters to handle date conversion for plotting
    register_matplotlib_converters()

    # modify plot configuration
    # plot size in inches
    plt.rc("figure", figsize=(16, 12))
    # font size in inches
    plt.rc("font", size=13)

    # prepare data for analysis
    if (dataSet == 'Salt Creek'):
        df = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\SaltCreek\reclassified_data\reclassed_monthly_0026_after2000.csv')
        transectBase = "usa_CA_0026-"
    else:
        df = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\SantaClara\reclassified_data\reclassified_monthly_0088_after2000.csv')
        transectBase = "usa_CA_0088-"


    # merge transect data
    transect = transectBase + transectNumber

    # convert date column to datetime format
    df['dates'] = pd.to_datetime(df['timestamp'])

    # filter data to only include user specified years
    filteredDF = df[(df['dates'].dt.year <= endYear) & (df['dates'].dt.year >= startYear)]

    # extract transect data into a series
    transectSeries = pd.Series(filteredDF[transect].values, index=filteredDF['dates'])

    # get statistics
    transectSeries.describe()

    # perform SLT analysis
        # seasonal must be ODD so that the window of estimation
        # can be centered around each point
    stl = STL(transectSeries, seasonal = 13, robust=True, seasonal_deg = 0, trend_deg = 0, low_pass_deg = 0 )
    results = stl.fit()

    # save results to df then to csv
    # trendDF = pd.Dataframe(results.trend )
    # to_csv("trend.csv")
    # seasonalData = pd.DataFrame(results.seasonal)
    # seasonalData.to_csv("seasonal.csv")
    # to_csv("results.csv")

    # plot results
    fig = results.plot()
    plt.show()

main()



