from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import spotipy.util as util
import sys
import numpy as np
import re
import datetime
import os
import pandas as pd
import argparse
from user_details import client_id, client_secret
import user_details
 #making some change
class SpotifyPlayListData():
    def __init__(self):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=user_details.client_id,
                                                            client_secret=user_details.client_secret)
        self.username='akipper96'
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

        #my playlists
        self.playlists = self.sp.user_playlists('1259766734')
        self.playlist_uris = [p_list['uri'] for p_list in self.playlists['items']]
        self.playlist_names = [re.compile('[^a-zA-Z0-9]').sub('',p_list['name']) for p_list in self.playlists['items']]
        # print self.playlist_names


    def get_PL_songs_and_artists(self,uri):
        playlist_id = uri.split(':')[2]
        results = self.sp.user_playlist(self.username,playlist_id,fields='name,tracks,next')
        tracks = results['tracks']
        artists = []
        names = []
        sslerr = 0
        for t in tracks['items']:
            try:
                names.append(t['track']['name'].encode('ascii','ignore'))
                #if there are multiple artists on the track, put them together with ' + '
                artists_on_track = ""
                for n, artist in enumerate(t['track']['artists']):
                    if n == len(t['track']['artists'])-1:
                        artists_on_track += artist['name']
                    else:
                        artists_on_track += artist['name']+" + "
                artists.append(artists_on_track)
            except:
                sslerr+=1
                try:
                    print(t['track']['name'])
                except:
                    pass
            #get all the batches of song data while there are no more left
        while tracks['next']:
            tracks = self.sp.next(tracks)
            for t in tracks['items']:
                try:
                    names.append(t['track']['name'].encode('ascii','ignore'))
                    artists_on_track = ""
                    for n, artist in enumerate(t['track']['artists']):
                        if n == len(t['track']['artists'])-1:
                            artists_on_track += artist['name']
                        else:
                            artists_on_track += artist['name']+" + "
                    artists.append(artists_on_track)
                except:
                    sslerr+=1
                    print (t)
                    try:
                        print (t['track']['name'])
                    except:
                        pass
        return names, artists

    def collect_playlist_data(self,uri):
        # username = uri.split(':')[2]
        playlist_id = uri.split(':')[2]
        results = self.sp.user_playlist(self.username,playlist_id,fields='name,tracks,next')

        #make sure we can save a file w/ the playlist name
        playlist_name = re.compile('[^a-zA-Z0-9]').sub('',results['name'])
        print("Getting songs from : %s" %(playlist_name))
        #if we're doing discover weekly, add the date
        pname = ''
        if playlist_name == 'DiscoverWeekly':
            playlist_name = 'DiscoverWeekly_'+datetime.datetime.now().strftime("%d-%m-%y")
            pname = 'DWeekly'
        if playlist_name == 'ReleaseRadar':
            playlist_name = 'ReleaseRadar_'+datetime.datetime.now().strftime("%d-%m-%y")
            pname = 'RRadar'
        print(playlist_name)
        #problem with playlist names when making file... some playlist names have odd characters in them (namely slashes)

        # all the data we want to collect from the songs
        tempo = []
        speechiness = []
        acousticness = []
        instrumentalness = []
        danceability = []
        loudness = []
        valence = []
        popularity = []
        duration_ms = []
        names = []
        artists = []

        energy = []
        liveness = []
        mode = []
        time_signature = []
        key = []
        explicit = []
        release_date = []

        uris = []

        #collect the data from the first batch of results
        tracks = results['tracks']
        if len(tracks['items'])==0:
            return

        #figured out that you have to import the package again if you edit the source code and you're using a Hydrogen Python kernel

        # SSLError COMES UP IF THE SONG IS LOCAL!!! IN WHICH CASE WE DON'T HAVE AUDIO FEATURES
        # for now lets just skip the songs that are local
        # however we can avoid the try statement if we just check if the song is local at the beginning
        # also a song called Santori by Raar in the house playlist

        #number of songs that return SSLError
        sslerr = 0
        for t in tracks['items']:
            try:
                names.append(t['track']['name'].encode('ascii','ignore'))
                #if there are multiple artists on the track, put them together with ' + '
                artists_on_track = ""
                for n, artist in enumerate(t['track']['artists']):
                    if n == len(t['track']['artists'])-1:
                        artists_on_track += artist['name']
                    else:
                        artists_on_track += artist['name']+" + "
                artists.append(artists_on_track)
                duration_ms.append(float(t['track']['duration_ms']))
                popularity.append(float(t['track']['popularity']))
                explicit.append(t['track']['explicit'])
                release_date.append(t['track']['album']['release_date'])
                uris.append(t['track']['uri'])

                #get the audio features for each track
                features = self.sp.audio_features(str(t['track']['uri']))
                energy.append(float(features[0]['energy']))
                time_signature.append(float(features[0]['time_signature']))
                mode.append(float(features[0]['mode']))
                liveness.append(float(features[0]['liveness']))
                key.append(float(features[0]['key']))
                tempo.append(float(features[0]['tempo']))
                speechiness.append(float(features[0]['speechiness']))
                acousticness.append(float(features[0]['acousticness']))
                instrumentalness.append(float(features[0]['instrumentalness']))
                danceability.append(float(features[0]['danceability']))
                loudness.append(float(features[0]['loudness']))
                valence.append(float(features[0]['valence']))
            except:
                sslerr+=1
                try:
                    print(t['track']['name'])
                except:
                    pass
        #get all the batches of song data while there are no more left
        while tracks['next']:
            tracks = sp.next(tracks)
            for t in tracks['items']:
                try:
                    names.append(t['track']['name'].encode('ascii','ignore'))
                    artists_on_track = ""
                    for n, artist in enumerate(t['track']['artists']):
                        if n == len(t['track']['artists'])-1:
                            artists_on_track += artist['name']
                        else:
                            artists_on_track += artist['name']+" + "
                    artists.append(artists_on_track)
                    duration_ms.append(float(t['track']['duration_ms']))
                    popularity.append(t['track']['popularity'])
                    explicit.append(t['track']['explicit'])
                    release_date.append(t['track']['album']['release_date'])
                    uris.append(t['track']['uri'])

                    features = self.sp.audio_features(str(t['track']['uri']))
                    energy.append(float(features[0]['energy']))
                    time_signature.append(float(features[0]['time_signature']))
                    mode.append(float(features[0]['mode']))
                    liveness.append(float(features[0]['liveness']))
                    key.append(float(features[0]['key']))
                    tempo.append(float(features[0]['tempo']))
                    speechiness.append(float(features[0]['speechiness']))
                    acousticness.append(float(features[0]['acousticness']))
                    instrumentalness.append(float(features[0]['instrumentalness']))
                    danceability.append(float(features[0]['danceability']))
                    loudness.append(float(features[0]['loudness']))
                    valence.append(float(features[0]['valence']))
                except:
                    sslerr+=1
                    print (t)
                    try:
                        print (t['track']['name'])
                    except:
                        pass


        print ("Number of tracks that couldn't be processed in %s: %d" %(playlist_name,sslerr))
        for n,name in enumerate(names):
            names[n]="'"+str(name)+"'"

        most_danceable = np.argmax(danceability)
        most_danceable_string = "Most danceable song: %s by %s, %d%% danceable" %(names[most_danceable],artists[most_danceable],int(danceability[most_danceable]*100))
        print(most_danceable_string)
        most_popular = np.argmax(popularity)
        most_popular_string = "Most popular song: %s by %s, %d%% popular"%(names[most_popular],artists[most_popular],int(popularity[most_popular]))
        print(most_popular_string)
        #
        # if pname == 'DWeekly':
        #     tweetstring = "this weeks @Spotify Discover Weekly haul:\n %s\n %s" %(most_danceable_string, most_popular_string)
        #     tweet_sys_command = 'twitter -eabekipnis@yahoo.com set %s' %('"'+tweetstring+'"')
        #     os.system(tweet_sys_command)

        l = np.array(list(zip(names,artists,duration_ms,popularity,tempo,speechiness,acousticness,instrumentalness,danceability,loudness,valence,energy,time_signature,liveness, mode, key,explicit,release_date,uris)))
        cols = "name,artists,duration_ms,popularity,tempo,speechiness,acousticness,instrumentalness,danceability,loudness,valence,energy,time_signature,liveness,mode,key,explicit,release_date,uri".split(',')
        import pdb
        pdb.set_trace()
        d = pd.DataFrame(l, columns = cols)

        def do_audio_analyses():
            audiofeatures = pd.read_json(json.dumps(self.sp.audio_features([d.loc[i]['uri'] for i in range(len(d))])))

            #drop the audio features we don't want
            audiofeatures.drop(['analysis_url','duration_ms','id','track_href','type','uri'],axis=1,inplace=True)

            #get the audio analysis for each song
            audioanalysis = [self.sp.audio_analysis(d.loc[i]['uri']) for i in range(len(d))]

            #we want to get some sample (equal size) of the pitch and timbre vectors for each song
            #size of how big each of our data 'slices' are
            slicesize = 15
            #how many slices are we taking from each song?
            n_slices = 10

            pitch_dict = {
                0:'C',
                1:'C#',
                2:'D',
                3:'D#',
                4:'E',
                5:'E#',
                6:'F',
                7:'F#',
                8:'G',
                9:'G#',
                10:'A',
                11:'A#',
                12:'B'}

            p = pd.DataFrame()
            t = pd.DataFrame()
            for song in range(len(audioanalysis)):
                try:
                    #define the slices (different for each song)
                    lowerrange = [int(len(audioanalysis[song]['segments']))/n_slices*i for i in range(n_slices)]
                    upperrange = [int(len(audioanalysis[song]['segments']))/n_slices*i+slicesize for i in range(n_slices)]

                    #define slicing for the array
                    s = [slice(lowerrange[i],upperrange[i]) for i in range(len(upperrange))]

                    pitches = np.array([[audioanalysis[song]['segments'][s[i]][k]['pitches'] for k in range(slicesize)] for i in range(n_slices)])
                    pitches = pd.DataFrame(pitches.flatten()).T
                    pitches.rename(columns=lambda x: 'segment%d unit%d %s' %((x/(slicesize*12)),(x%(slicesize*12)/12),pitch_dict[x%(slicesize*12)%12]),inplace=True)
                    p = p.append(pitches)

                    timbre = np.array([[audioanalysis[song]['segments'][s[i]][k]['timbre'] for k in range(slicesize)] for i in range(n_slices)])
                    timbre = pd.DataFrame(timbre.flatten()).T
                    timbre.rename(columns=lambda x: 'segment%d unit%d %s' %((x/(slicesize*12)),(x%(slicesize*12)/12),'timbre'),inplace=True)
                    t = t.append(timbre)
                except:
                    d.drop([song],inplace=True)
                    audiofeatures.drop([song],inplace=True)
            d = pd.concat([d,audiofeatures,t.reset_index(),p.reset_index()],axis=1)

            d.to_csv('~/Desktop/Data_Science/SPOTIPY/playlists_data/%s_playlist_song_data.csv' %(playlist_name),encoding ='utf-8')

    def get_discover_weekly(self,dw,rr):
        for n,uri in enumerate(self.playlist_uris):
            if rr and self.playlist_names[n]=='ReleaseRadar':
                self.collect_playlist_data(uri)
            if dw and self.playlist_names[n]=='DiscoverWeekly':
                self.collect_playlist_data(uri)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dw', help='Discover Weekly', action='store_true')
    parser.add_argument('--rr', help='Release Radar', action='store_true')
    args = parser.parse_args()
    spd = SpotifyPlayListData()
    spd.get_discover_weekly(args.dw, args.rr)
