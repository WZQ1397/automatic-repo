echo off
set copyPath=GTJAQH_WEBSITE_db_%date:~0,4%%date:~5,2%%date:~8,2%0300.BAK
copy D:\dbbak\%copyPath% Z:\%copyPath%