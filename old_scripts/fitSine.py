# import libraries
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def main():

    # set filepath
    # filePath = r'C:\Users\kenyo\shorelineAnalysis\SaltCreek\biweekly_seasonal_monthly_means.csv'
    # filePath = r'C:\Users\kenyo\shorelineAnalysis\SaltCreek\rawdata_monthly_means.csv'
    # filePath = r'C:\Users\kenyo\shorelineAnalysis\SaltCreek\monthly_mean_shoreline_position\all_monthly_shoreline_position_means.csv'
    filePath= r'/data_investigation/missing_data/missing_data_monthly_means.csv'

    # load csv into a dataframe
    df = pd.read_csv( filePath )

    # for a specific transect
    transectID = '0004'

    # set transect
    transect_base = 'usa_CA_0003-'
    transect = transect_base + transectID + '_mean'

    # y = A*sin(Bx+C)+D
    def sine_function(x, amplitude, frequency, phase, offset):
        return amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset

    # save time stamps to an array
    x_data = df['timestamp'].values

    # save monthly mean shoreline positions to an array
    y_data = df[transect].values

    guess_freq = 1 # freq is B
    # guess_amplitude = np.std(y_data)**2 # amp is A
    guess_amplitude = 1
    guess_phase = 0 # phase is C
    guess_offset =  np.mean(y_data) # offset is D

    # save initalize guesses to an array
    initial_guess = [guess_freq, guess_amplitude, guess_phase, guess_offset]

    # Perform the curve fitting
    params, params_covariance = curve_fit(sine_function, x_data, y_data, p0=initial_guess)

    amplitude_fit, frequency_fit, phase_fit, offset_fit = params

    # Generate the fitted curve using the fitted parameters
    y_fit = sine_function(x_data, amplitude_fit, frequency_fit, phase_fit, offset_fit)

    # print the sine function
    print("Sine Function: y = {} * sin(2*pi*{}*x + {}) + {}".format(amplitude_fit, frequency_fit, phase_fit, offset_fit))

    # plot
    plt.scatter(x_data, y_data, label='Monthly Mean Shoreline Position')
    plt.plot(x_data, y_fit, label='Fitted Sine Function', color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid()
    plt.show()

main()