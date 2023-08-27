# calfornia-coastal-change
This branch is for CoastSeg data which uses different nomenclature and numbering systems than CoastSat. 
Program Process: analyzes shoreline position data by resampling, interpolating, 
detrending, and generating basic statistics on data
<br><br>
Input/Parameters: filepath to raw CoastSeg transect data 
<br><br>
Output: 4 unique CSV's: amplitude, <br>
month of maximum shoreline position for that transect, <br>
month of minimum shoreline position for that transect, <br>
monthly mean detrended shoreline positions for each transect 
<br><br>
Dependencies: pandas, calendar, statsmodels, matplotlib
