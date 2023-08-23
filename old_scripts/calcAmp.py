# import libraries
import pandas as pd

def main():

    # get user input
    filePath = input("Filepath: ")

    calc_amplitude( filePath )

def calc_amplitude( csvFilePath ):

    # store csv into dataframe
    df = pd.read_csv( csvFilePath )

    # convert to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    beachID = csvFilePath[67:71]

    # new df to store upcoming amplitude data
    ampDF = pd.DataFrame(columns=['transectID', 'amplitude'])

    for col in df.columns[1:]:
        transect_id = col[0:16]
        max_position = df[col].max()
        min_position = df[col].min()
        amplitude = (max_position - min_position) / 2
        ampDF = pd.concat([ampDF, pd.DataFrame({'transectID': [transect_id], 'amplitude': [amplitude]})], ignore_index=True)

    ampDF.to_csv('amplitude_{}_seasonal.csv'.format(beachID))

main()














