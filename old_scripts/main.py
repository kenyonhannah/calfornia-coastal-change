# import libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.api as sm

# main function
def main():
    # initalize variables
    transectBase = "usa_CA_0088-"

    # get user input
    transectNumber = input("Transect number [0000 - 0096] : ")
    userYear = input("What year would you like to look at? ")
    userStartYear = input("What year would you like to start at? ")
    userEndYear = input("What year would you like to end at? ")

    # datatype transfers
    year = int(userYear)
    startYear = int(userStartYear)
    endYear = int(userEndYear)

    # merge transect data
    transect = transectBase + transectNumber

    # establishBaselineStats
    smoothScatterplot(transect, year, startYear, endYear)


def smoothScatterplot(transect, year, startYear, endYear):

    # import csv into dataframes
    santaClaraShorelines = pd.read_csv(r'C:\Users\kenyo\Desktop\USGS\SampleData\SantaClaraEvent\usa_CA_0088_time_series.csv')

    # remove excess time data
    santaClaraShorelines['dates'] = santaClaraShorelines['dates'].str.slice(stop=10)

    # convert 'dates' column in csv to matplotlib acceptable datatime format
    santaClaraShorelines['Date'] = pd.to_datetime(santaClaraShorelines['dates'], format="%Y-%m-%d")

    # collect data from specified year
    filteredDF = santaClaraShorelines[santaClaraShorelines['Date'].dt.year == year]

    # convert datetime data into numerical representation for graphing ease
    filteredDF.loc[:, 'Date'] = mdates.date2num(filteredDF['Date'])

    # still show datetime format on x axis NOT numerical representation
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # compute lowess fit
    lowess = sm.nonparametric.lowess(filteredDF[transect], filteredDF['Date'])

    # create the scatterplot
    sns.scatterplot(data=filteredDF, x="Date", y=transect)

    # plot lowess fit
    sns.lineplot(x=lowess[:, 0], y=lowess[:, 1], color='red')

    # formatting chart
    plt.title("Shoreline Position over time with Lowess Fit")
    plt.xlabel("Date")
    plt.ylabel("Shoreline Position")
    plt.show()

    # get residuals

    # show residuals


main()