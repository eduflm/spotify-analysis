from database import Database


TRAINING_PORCENTAGE = 0.7

#Dado de Entrada

# Week, Month, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Valence, Tempo

#Saida

#Porcentagem [Top 10, Top 50, Top 100, Top 200]

class DataPreparation:

    def __init__(self):
        self.x_training = []
        self.y_training = []

        self.x_test = []
        self.y_test = []

        self.database = Database()
    
    def get_track_basic_info(self):
        charts = self.database.get_all_charts()
        tracks = self.database.get_all_track_basic_info()
        pass

if __name__ == "__main__":
    DataPreparation().get_track_basic_info()

