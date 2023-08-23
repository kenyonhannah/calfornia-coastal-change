# import libraries
import pandas as pd

def main():

    # get user input
    # filepath_resampled = input("resampled data filepath: ")
    # filepath_trend = input("Trend data filepath: ")
    filepath_resampled = r'C:\Users\kenyo\shorelineAnalysis\SantaClara\reclassified_data\reclassified_monthly_0088_after2000.csv'
    filepath_trend = r'C:\Users\kenyo\shorelineAnalysis\SantaClara\stl_trend_results_0088.csv'
    filepath_detrended_data = r'C:\Users\kenyo\shorelineAnalysis\SantaClara\detrended_data_0088.csv'

    # detrend data
    # detrend( filepath_resampled, filepath_trend )
    plot_residuals( filepath_detrended_data )

def detrend( csv_filepath_resampled, csv_filepath_trend ):

    # load csv's into dataframes
    resampled_data = pd.read_csv( csv_filepath_resampled )
    trend_data = pd.read_csv( csv_filepath_trend )

    # convert dates to datetime
    resampled_data['timestamp'] = pd.to_datetime( resampled_data['timestamp'] )
    trend_data['timestamp'] = pd.to_datetime( trend_data['timestamp'])

    # initalize data new dataframe
    detrendedDF = pd.DataFrame()

    # for each column in resampled data
    for col in resampled_data.columns[1:]:
        if ( col != 'timestamp'):
            # subtract trend data from resampled data
            detrendedDF[col] = trend_data[col] - resampled_data[col]

    # reset index
    detrendedDF.set_index( resampled_data['timestamp'], inplace=True)

    # store dataframe to csv
    detrendedDF.to_csv( "detrended_data.csv" )

def plot_residuals( csv_filepath_detrended_data ):

    # save csv data to dataframe

    #

main()

