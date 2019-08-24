from pymongo import MongoClient

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
