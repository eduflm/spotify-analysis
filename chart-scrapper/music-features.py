import os
import sys
import json

import urllib.request

from database import Database

class AudioFeatures:

    def __init__(self, track_basic_id, duration, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo):
        self.track_basic_id = track_basic_id
        self.duration = duration
        self.key = key
        self.mode = mode
        self.time_signature = time_signature
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo


class APIScrapper:

    def __init__(self, app_key, oauth_key):
        #max 100 ids
        self.api_link = "https://api.spotify.com/v1/audio-features?ids=" 
        self.app_key = app_key
        self.oauth_key = oauth_key
        self.musics_with_features = []
    
    def get_audio_features(self, ids):
        max_ids = 100
        for i in range(0, len(ids), max_ids):
            group = ids[i: i + max_ids]
            ids_for_link = ",".join(group)
            
            final_link = self.api_link+ids_for_link
            header = {'Authorization': 'Bearer ' + oauth_key}

            request = urllib.request.Request(final_link, headers=header)
            response = urllib.request.urlopen(request)
            response_in_json = json.loads(response.read())

            print(response_in_json)

            for music in response_in_json['audio_features']:
                track_basic_id = music["id"]
                duration = music["duration_ms"]
                key = music["key"]
                mode = music["mode"]
                time_signature = music["time_signature"]
                acousticness = music["acousticness"]
                danceability = music["danceability"]
                energy = music["energy"]
                instrumentalness = music["instrumentalness"]
                liveness = music["liveness"]
                loudness = music["loudness"]
                speechiness = music["speechiness"]
                valence = music["valence"]
                tempo = music["tempo"]
                
                music_with_features = AudioFeatures(track_basic_id,duration,key,mode,time_signature,acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo)

                self.musics_with_features.append(music_with_features)

        database = Database()

        database.insert_audio_features(self.musics_with_features)

        return 


if __name__ == "__main__":
    key_filename = './spotify-keys'
    if not os.path.isfile(key_filename):
        print("É necesário especificar um arquivo info com as keys para acessar o spotify")
        sys.exit()

    keys_file = open(key_filename, "r").read().splitlines()

    app_key = keys_file[0]
    oauth_key = keys_file[1]
    
    api_scrapper = APIScrapper(app_key, oauth_key)

    database = Database()
    ids = database.get_tracks_id();

    api_scrapper.get_audio_features(ids)


"layers=" =  str(configuration)
"last_loss=" =  str(mlp_classifier.loss_)
"last_iteration=" =  str(mlp_classifier.n_iter_)
"training_score=" =  str(training_set_score)
"test_score=" =  str(test_set_score)
"time_elapsed=" =  str(time_elapsed)