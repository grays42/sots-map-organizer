![screenshot of output](https://i.imgur.com/0h0HAVs.png)

Simple script file to take all of the custom maps from the Sword of the Stars "Custom Maps" guide (https://steamcommunity.com/sharedfiles/filedetails/?id=3002390160) and remove all but the most important variants.

1. Place the python script in the SotS directory (with the exe file) after you have unpacked the provided maps into the Maps directory.
2. The python file will scan the Maps directory, identify each map "series" and the number of maps in it, and whitelist only the most important 5 maps
3. All other maps will be moved to an "Archived_Maps" directory.

The "most important 5 maps" for each map series are:
- the lowest star count (0th percentile)
- the highest star count (100th percentile)
- the median (50th percentile)
- the 25th and 75th percentile star counts

The only series that is a bit wonky is the Ring of Clusters series because of its naming convention, but it still gets rid of *most* of the duplicates and leaves you with 34 good maps instead of 253.
