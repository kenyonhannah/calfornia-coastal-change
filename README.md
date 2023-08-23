# calfornia-coastal-change
Program Process: analyzes shoreline position data by resampling, interpolating, 
detrending, and generating basic statistics on data
<br><br>
Input/Parameters: filepath to raw CoastSat transect data 
<br><br>
Output: 4 unique CSV's: amplitude, 
month of maximum shoreline position for that transect, 
month of minimum shoreline position for that transect, 
monthly mean detrended shoreline positions for each transect 
<br><br>
Dependencies: pandas, calendar, statsmodels, matplotlib
