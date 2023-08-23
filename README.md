# calfornia-coastal-change

Program Process: analyzes shoreline position data by resampling, interpolating, 
detrending, and generating basic statistics on data 
Input/Parameters: filepath to raw CoastSat transect data 
Output: 4 unique CSV's: amplitude, 
month of maximum shoreline position for that transect, 
month of minimum shoreline position for that transect, 
monthly mean detrended shoreline positions for each transect 
Dependencies: pandas, calendar, statsmodels, matplotlib
