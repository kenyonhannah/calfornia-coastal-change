# import libraries
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm 

# main function
def main():
    # initalize variables
    transectBase = "usa_CA_0088-"

    # get user input  
    transectNumber = input("Transect number [0000 - 0096] : ")

    # merge transect data
    transect = transectBase + transectNumber
    
    # define a search window for event
    searchWindow = input("Define a search window for the event [# of months]: ")

    # establishBaselineStats
    smoothScatterplot(transect)
    
def smoothScatterplot(transect):
    
    # import csv into dataframes
    santaClaraShorelines = pd.read_csv(r'C:\Users\kenyo\Desktop\USGS\SampleData\SantaClaraEvent\usa_CA_0088_time_series.csv')

    # convert 'dates' column in csv to datatime format
    santaClaraShorelines['Date'] = pd.to_datetime(santaClaraShorelines['dates'])

    # plot scatterplot
    plt.scatter(santaClaraShorelines['Date'], santaClaraShorelines[transect])
    plt.xlabel('Time')
    plt.ylabel('Values')

    # compute lowess fit
                                             # y values                     # x values 
    lowess_fit = sm.nonparametric.lowess(santaClaraShorelines[transect], santaClaraShorelines['Date'])
    LowessFit = pd.DataFrame(lowess_fit)
    print(LowessFit)

    # show plot
    plt.scatter(santaClaraShorelines['Date'], santaClaraShorelines[transect], label = 'Raw Data')
    plt.plot( lowess_fit[:, 0], lowess_fit[:, 1], 'bo', label = 'Lowess Smoothing')
    plt.xlabel('Time')
    plt.ylabel('Shoreline Position')
    plt.title('Shoreline Position over time with Lowess Smoothing')
    plt.legend()
    plt.show()

    # get residuals

    # show residuals

main()




        

