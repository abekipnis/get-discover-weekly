# get-discover-weekly
I was frustrated with having to listen to my Discover Weekly and Release Radar playlists every week; I wish there was a way I could further sift through my music recommendations. This is a command line tool that grabs the discover weekly and/or release radar playlist from your Spotify account and reports the most 'danceable' and most popular song. It also saves a .csv file with all the song data from those playlists. These data include name, artists, duration, popularity, tempo, speechiness, acousticness, instrumentalness, danceability, loudness, valence, energy, time signature, liveness, mode, key, explicit, and release date. Look [here](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) for an explanation of the audio features, i.e. valence, energy, acousticness, danceability, etc. 

This program requires the [spotipy](https://spotipy.readthedocs.io/) Python library (as well as Numpy and Pandas), which can all be installed using pip. 

This program also requires a Spotify developer / application client id and secret, which can be created by going [here](https://developer.spotify.com/dashboard/applications) and clicking 'create a client id'. Then, copy the client ID and client secret to the declarations in the user_details.py file, or add them as environment variables by writing in your ~/.zshrc or ~/.bashrc file

`export SPOTIFY_CLIENT='client id here'`

`export SPOTIFY_SECRET='secret here'` 

and then sourcing the rc file with `source ~/.zshrc` on the terminal.

Lastly, to make the code work to save the .csv files, edit the line in get_discover_weekly.py that says `        d.to_csv('~/Desktop/Data_Science/SPOTIPY/playlists_data/%s_playlist_song_data.csv' %(playlist_name),encoding ='utf-8')`. Change the path to a location where you would like to save your data. 

To set up an alias to run this script directly from the command line, without having to navigate to the python executable path every time you run the code, replace `~/Desktop/Data_Science/SPOTIPY/gdw/` with the directory where the .py files are stored, and add these lines below to ~/.zprofile or ~/.bash_profile (depending on which shell you're using). Then run `source ~/.zprofile` to source the changes.

`alias gdw="python ~/Desktop/Data_Science/SPOTIPY/gdw/get_discover_weekly.py --dw"`

`alias grr="python ~/Desktop/Data_Science/SPOTIPY/gdw/get_discover_weekly.py --rr"`

Then, typing `grr` or `gdw` on the command line will get the Release Radar or Discover Weekly playlist data. 
