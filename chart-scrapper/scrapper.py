import requests
import sys
import json
import os

from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup

from track import Track
from database import Database


class Scrapper: 

    def __init__(self):
        self.base_link = "https://spotifycharts.com/regional/"
        self.country = "br"
        self.frequency = "daily"
        self.start_date = date(2018, 4, 26)
        self.end_date = date(2018, 4, 27)
        self.current_date = self.start_date
        
        self.tracks = []
        self.session = requests.Session()
        self.database = Database()

        return

    
    def connect_to_web_site(self):
        link = self.get_full_link()
        print("Connecting to " + link)
        try:
            page = self.session.get(link, verify = False)
            if page.status_code == 200:
                print("Connected")
                self.scrap_info_from_page(page.text)
            else:
                print("Trying again to connect... " + link)
                page = self.session.get(link, verify = False)
                if page.status_code == 200:
                    print("Connected")
                    self.scrap_info_from_page(page.text)
                else:
                    print("Unable to connect to " + link + ". Reporting...")
                    with open("logfile", "a") as logFile:
                        logFile.write("- Unable to connect to "+link+" at " + str(datetime.now()) + " \n")
                        self.change_date()
        except Exception as e:
            print("Exception raised " + link + ". Reporting...")
            with open("logfile", "a") as logFile:
                logFile.write("- An exception was raised for "+link+" at " + str(datetime.now()) + ". Exception: " + str(e) + "\n")
                self.change_date()

    
    def get_full_link(self):
        return self.base_link + self.country + "/" + self.frequency + "/" + str(self.current_date)
    
    def change_date(self):
        self.current_date = self.current_date + timedelta(days=1)
    
    def should_stop(self):
        return self.current_date == self.end_date

    
    def scrap_info_from_page(self, page_text):
        beautiful_soup = BeautifulSoup(page_text, "html.parser")
        for track_component in beautiful_soup.find_all("tbody")[0].find_all("tr"):
            track_artist = track_component.find_all("td", {"class": "chart-table-track"})[0].find_all("span")[0].text
            track_name = track_component.find_all("td", {"class": "chart-table-track"})[0].find_all("strong")[0].text
            track_streams = int(track_component.find_all("td", {"class": "chart-table-streams"})[0].text.replace(",",""))
            track_link = track_component.find_all("td", {"class": "chart-table-image"})[0].find_all("a", href=True)[0]['href']
            track_image_link = track_component.find_all("td", {"class": "chart-table-image"})[0].find_all("a", href=True)[0].find_all("img")[0]['src']
            track_chart_position = int(track_component.find_all("td", {"class": "chart-table-position"})[0].text)
            track_trend = self.define_trend(track_component)

            new_track = Track(track_artist, track_name, track_streams, track_link, track_image_link, track_chart_position, track_trend, self.current_date)

            # print(new_track.to_json())

            self.tracks.append(new_track)
        
        self.database.write_tracks(self.tracks)
        self.tracks = []
        self.change_date()
    
    #Unused
    def write_file(self):
        folder_name = "data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_path = "data/"+str(self.current_date)+".json"
        print("writing in file: " + file_path)
        with open(file_path, 'w') as output_file:
            json.dump(self.tracks, output_file)
        self.track = []
        print("Done! The file " + file_path + " was created!")
    
    def define_trend(self, track_component):
        svg = track_component.find_all("svg")[0]
        if svg.find('rect') :
            return "neutral"
        elif svg.find('circle'):
            return "new"
        else:
            points = svg.find_all('polygon')[0]['points']
            points = points.replace(" ","")
            if points == "0912963":
                return "up"
            elif points == "1230369":
                return "down"
            else:
                return "undefined"

        


if __name__ == "__main__":
    print("Hello World")
    scrapper = Scrapper()
    while not scrapper.should_stop():
        scrapper.connect_to_web_site()