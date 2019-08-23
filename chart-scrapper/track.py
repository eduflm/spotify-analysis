import json

class Track:
    def __init__(self, artist, track_name, number_of_streams, track_link, image_path, chart_position, trend):
        self.track_artist = self.get_track_artist(artist);
        self.track_name = track_name
        self.track_number_of_streams = number_of_streams
        self.track_link = track_link
        self.track_image_path = image_path
        self.track_chart_position = chart_position
        self.trend = trend
        self.track_id = self.get_track_id()
    
    def get_track_id(self):
        return self.track_link.replace("https://open.spotify.com/track/","")
    
    def get_track_artist(self, track_name):
        by = track_name[0:3]
        if by == "by ":
            return track_name[3:]
        return track_name
    
    def __str__(self):
        string = "Track name: " + self.track_name + "\n" + "Artist: " + self.track_artist + "\n" + "Number of streams: " + str(self.track_number_of_streams) + "\n" + "Current date: " + self.current_date + "\n" + "Track link: " + self.track_link + "\n" + "Image path: " + self.track_image_path + "\n" + "Chart Position: " + str(self.track_chart_position) + "\n"
        return string
    
    # def get_dict(self):
    #     return {
    #         "Name" : self.track_name,
    #         "Artist" : self.track_artist,
    #         "NumberOfStreams" : self.track_number_of_streams,
    #         "Link" : self. 
    #     }
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
