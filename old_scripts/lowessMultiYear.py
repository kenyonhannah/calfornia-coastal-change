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
    userStartYear = input("What year would you like to start at? ")
    userEndYear = input("What year would you like to end at? ")
    userfrac = input("What fraction of the data should be used when estimating each y-value: ")

    # datatype transfers
    startYear = int(userStartYear)
    endYear = int(userEndYear)
    fraction = float(userfrac)

    # merge transect data
    transect = transectBase + transectNumber

    # run
    smoothScatterplot(transect, startYear, endYear, fraction)

    continueAnalysis = input("Would you like to analyze more data (y/n) ? ")
    print('\n')

    # while user still wants to continue
    while continueAnalysis == 'y':

        # user input
        transectNumber = input("Transect number [0000 - 0096] : ")
        userStartYear = input("What year would you like to start at? ")
        userEndYear = input("What year would you like to end at? ")
        userfrac = input("What fraction of the data should be used when estimating each y-value: ")
        print('\n')

        # datatype transfers
        startYear = int(userStartYear)
        endYear = int(userEndYear)
        fraction = float(userfrac)

        # merge transect data
        transect = transectBase + transectNumber
        smoothScatterplot(transect, startYear, endYear, fraction)


def smoothScatterplot(transect, startYear, endYear, fraction):

    # prepare data for analysis
    # import csv into dataframes
    santaClaraShorelines = pd.read_csv(
        r'C:\Users\kenyo\Desktop\USGS\SampleData\SantaClaraEvent\usa_CA_0088_time_series.csv')

        # remove hours, seconds, minutes from 'dates' column
    santaClaraShorelines['dates'] = santaClaraShorelines['dates'].str.slice(stop=10)

        # convert 'dates' column in csv to datatime format for matplotlib processing purposes
    santaClaraShorelines['Date'] = pd.to_datetime(santaClaraShorelines['dates'], format="%Y-%m-%d")

        # filter data to only include user specified years
    filteredDF = santaClaraShorelines[(santaClaraShorelines['Date'].dt.year <= endYear) & (santaClaraShorelines['Date'].dt.year >= startYear)]

        # convert datetime data into numerical representation for plotting ease
    filteredDF.loc[:, 'Date'] = mdates.date2num(filteredDF['Date'])

        # still show datetime format on x axis NOT numerical representation
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # data analysis
        # compute lowess fit
    lowess = sm.nonparametric.lowess(filteredDF[transect], filteredDF['Date'], frac= fraction)

    # show plots
        # create the scatterplot
    sns.scatterplot(data = filteredDF, x = "Date", y = transect)
        # plot lowess fit
    sns.lineplot(x = lowess[:, 0], y = lowess[:, 1], color = 'red')
    plt.title("Shoreline Position over time with Lowess Fit")
    plt.xlabel("Date")
    plt.ylabel("Shoreline Position")

        # display plots
    plt.show()

main()