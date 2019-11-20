from pymongo import MongoClient
import isodate

class Database:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['spotify_analysis']
    
    def write_tracks(self, list_of_tracks):
        track_basic_info_collection = self.db.track_basic_info
        chart_collection = self.db.chart
        for track in list_of_tracks:
            track_basic_info = track_basic_info_collection.find_one({"spotify_track_id": track.track_id})
            track_basic_info_id = None
            if track_basic_info == None:
                #Fluxo onde a entidade básica não está cadastrada no banco
                track_basic_info_id = track_basic_info_collection.insert_one({
                    "spotify_track_id" : track.track_id,
                    "name" : track.track_name,
                    "artist" : track.track_artist,
                    "track_link" : track.track_link,
                    "track_image" : track.track_image_path
                }).inserted_id
            else :
                #Fluxo onde a entidade básica já entá cadastrada no banco
                track_basic_info_id = track_basic_info['_id']
            
            chart_collection.insert_one({
                "track_basic_info_id" : track_basic_info_id,
                "date" : track.date,
                "chart_position" : track.track_chart_position,
                "number_of_streams" : track.track_number_of_streams,
                "trend" : track.trend
            })
        
    def insert_audio_features(self, audio_features):
        track_basic_info_collection = self.db.track_basic_info
        for audio_feature in audio_features:
            basic_id = audio_feature.track_basic_id
            find_query = {"spotify_track_id" : basic_id}
            update = track_basic_info_collection.update_one(find_query, { "$set" : {"features" : {
                "duration" : audio_feature.duration,
                "key" : audio_feature.key,
                "mode" : audio_feature.mode,
                "time_signature" : audio_feature.time_signature,
                "acousticness" : audio_feature.acousticness,
                "danceability" : audio_feature.danceability,
                "energy" : audio_feature.energy,
                "instrumentalness" : audio_feature.instrumentalness,
                "liveness" : audio_feature.liveness,
                "loudness" : audio_feature.loudness,
                "speechiness" : audio_feature.speechiness,
                "valence" : audio_feature.valence,
                "tempo" : audio_feature.tempo
            }}
            })
        print("Músicas inseridas com sucesso!")
        
    def get_tracks_id(self):
        track_basic_info_collection = self.db.track_basic_info
        tracks_ids = track_basic_info_collection.find({}, {"spotify_track_id" : 1})
        ids = []
        for track_id in tracks_ids:
            ids.append(track_id['spotify_track_id'])
        return ids
    
    def get_week(self, day_of_the_month):
        if day_of_the_month <= 8:
            return 1
        elif day_of_the_month <= 16:
            return 2
        elif day_of_the_month <= 24:
            return 3
        else:
            return 4
    
    def normalize_dates(self):
        charts_collection = self.db.chart
        charts = charts_collection.find()

        for chart in charts:
            chart_id = chart["_id"]
            day = int(chart['date'].day)
            month = int(chart['date'].month)
            week = self.get_week(day)
            update = charts_collection.update_one({"_id" : chart_id}, {"$set" : {"week" : week, "month" : month}})
            print("Chart " + str(chart_id) + " updated")
    
    def get_all_charts(self):
        charts_collection = self.db.chart
        charts = charts_collection.find()
        return charts
    
    def get_all_track_basic_info(self):
        track_basic_info = self.db.track_basic_info
        tracks = track_basic_info.find()
        return tracks
    
    def get_all_models(self):
        model = self.db.model
        models = model.find()
        return models
    
    def create_track_cache(self):
        track_basic_info = self.db.track_basic_info
        tracks = track_basic_info.find()

        cache = {}

        for track in tracks:
            cache[track['_id']] = track
        
        return cache
    
    def create_one_table(self):
        charts_collection = self.db.chart
        charts = charts_collection.find()
        
        tracks = self.create_track_cache()

        models = []

        for chart in charts:
            basic_info_id = chart['track_basic_info_id']
            track = tracks[basic_info_id]

            model = {
                "music_name" : track['name'],
                "artist" : track['artist'],
                "first_week": 1 if chart['week'] == 1 else 0,
                "second_week": 1 if chart['week'] == 2 else 0,
                "third_week": 1 if chart['week'] == 3 else 0,
                "fourth_week": 1 if chart['week'] == 4 else 0,
                "january": 1 if chart['month'] == 1 else 0,
                "february": 1 if chart['month'] == 2 else 0,
                "march": 1 if chart['month'] == 3 else 0,
                "april": 1 if chart['month'] == 4 else 0,
                "may": 1 if chart['month'] == 5 else 0,
                "june": 1 if chart['month'] == 6 else 0,
                "july": 1 if chart['month'] == 7 else 0,
                "august": 1 if chart['month'] == 8 else 0,
                "september": 1 if chart['month'] == 9 else 0,
                "october": 1 if chart['month'] == 10 else 0,
                "november": 1 if chart['month'] == 11 else 0,
                "december": 1 if chart['month'] == 12 else 0,
                "acousticness" : track['features']['acousticness'],
                "danceability" : track['features']['danceability'],
                "energy" : track['features']['energy'],
                "instrumentalness" : track['features']['instrumentalness'],
                "liveness" : track['features']['liveness'],
                "loudness" : track['features']['loudness'],
                "speechiness" : track['features']['speechiness'],
                "valence" : track['features']['valence'],
                "tempo" : track['features']['tempo'],
                "artist" : track['artist'],
                "position" : chart['position']
            }

            models.append(model)

        dataset_collection = self.db.dataset
        dataset_collection.insert_many(models)

if __name__ == "__main__":
    dt = Database()
    dt.create_one_table()
