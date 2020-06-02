# get-discover-weekly
This is a command line tool that grabs the discover weekly and/or release radar playlist from your Spotify account and reports the most 'danceable' and most popular song. It also saves a .csv file with all the song data from those playlists. 

This program requires the [spotipy](https://spotipy.readthedocs.io/) Python library (as well as Numpy and Pandas), which can all be installed using pip. 

This program also requires a Spotify developer / application client id and secret, which can be created by going [here](https://developer.spotify.com/dashboard/applications) and clicking 'create a client id'. Then, copy the client ID and client secret to the declarations in the user_details.py file, or add them as environment variables by writing 

`export SPOTIFY_CLIENT='client id here'`

`export SPOTIFY_SECRET='secret here'` 

and then `source ~/.zshrc`. 

To set up an alias to run this script directly from the command line, without navigating to the python path every time, replace `~/Desktop/Data_Science/SPOTIPY/gdw/` with the directory where the .py files are stored, and add these lines below to ~/.zprofile or ~/.bash_profile (depending on which shell you're using). Then run `source ~/.zprofile` to source the changes.

`alias gdw="python ~/Desktop/Data_Science/SPOTIPY/gdw/get_discover_weekly.py --dw"`

`alias grr="python ~/Desktop/Data_Science/SPOTIPY/gdw/get_discover_weekly.py --rr"`
