# Week, Month, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Valence, Tempo


class NeuralNetworkModel:

    def __init__(self, week, month, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo, top10Probability = 0, top50Probability = 0, top100Probability = 0, top200Probability = 0):
        self.week = week
        self.month = month
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo
        self.top10Probability = top10Probability
        self.top50Probability = top50Probability
        self.top100Probability = top100Probability
        self.top200Probability = top200Probability

    def __repr__(self):
        return [self.week,self.month,self.acousticness,self.danceability,self.energy,self.instrumentalness,self.liveness,self.loudness,self.speechiness,self.valence,self.tempo]
    
    def print(self):
        print ([self.week,self.month,self.acousticness,self.danceability,self.energy,self.instrumentalness,self.liveness,self.loudness,self.speechiness,self.valence,self.tempo, self.top10Probability, self.top50Probability, self.top100Probability, self.top200Probability])



        



