
def reclassify():
    # save csv to df
    df = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\SaltCreek\coastSat_data\usa_CA_0026_time_series_single_test_transect.csv')

    # remove seconds, minutes, days
    df['timestamp'] = df['timestamp'].str.slice(stop=7)

    # set timestamp values to datetime datatype
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # filter data to only include years after 2000
    df = df[df['timestamp'].dt.year >= 2000]

    # add missing months
    df = add_missing_values(df)

    # interpolate missing values
    df = df.interpolate(method='linear', limit_direction='forward',limit_area='inside')

    # resample to monthly
    # create new df where shoreline position value is the mean of all values taken that month
    df = df.groupby(['timestamp'], as_index=False).mean()

    df.to_csv('reclassed_0026_0010.csv')

reclassify()
