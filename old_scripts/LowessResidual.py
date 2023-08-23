# import libraries
import matplotlib
matplotlib.use('TkAgg')
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
    userFracYear = input("What increment of time would you like to smooth over (years) : ")

    # datatype transfers
    startYear = int(userStartYear)
    endYear = int(userEndYear)
    fraction = float(userFracYear)
    fraction = fraction / (endYear - startYear)

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
        userFracYear = input("What increment of time would you like to smooth over (years) : ")
        print('\n')

        # datatype transfers
        startYear = int(userStartYear)
        endYear = int(userEndYear)
        fraction = float(userFracYear)
        fraction = fraction / (endYear - startYear)

        # merge transect data
        transect = transectBase + transectNumber
        smoothScatterplot(transect, startYear, endYear, fraction)
        continueAnalysis = input("Would you like to analyze more data (y/n) ? ")
        print('\n')


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

        # remove NaN so number of predictedValues is the same as actual values
    finalDF = filteredDF.copy()
    finalDF.dropna(inplace=True)

        # convert datetime data into numerical representation for plotting ease
    finalDF.loc[:, 'Date'] = mdates.date2num(finalDF['Date'])

    # data analysis
        # compute lowess fit
    lowess = sm.nonparametric.lowess(finalDF[transect], finalDF['Date'], frac= fraction)

        # get lowess values
    predictedValues = lowess[:, 1]

        # get residuals
    residuals = finalDF[transect] - predictedValues

    # show plots
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

    # apply datetime formating to xaxis on both subplots
    for ax in [ax1, ax2]:
        # apply formatting
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # first plot
    sns.scatterplot(data=finalDF, x="Date", y=transect, ax=ax1)
    sns.lineplot(x=lowess[:, 0], y=lowess[:, 1], color='red', ax=ax1)
    ax1.set_title("Shoreline Position over time with Lowess Fit")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Shoreline Position")

    # second plot
    ax2.scatter(finalDF["Date"], residuals, color='green', label='Residuals')
    ax2.set_title("Residuals")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Shoreline Position")

    # Adjust the spacing between subplots
    plt.tight_layout()

    plt.show()

main()