import requests
import sys
import json
import os

from datetime import date, timedelta

from bs4 import BeautifulSoup
from track import Track


class Scrapper: 

    def __init__(self):
        self.base_link = "https://spotifycharts.com/regional/"
        self.country = "br"
        self.frequency = "daily"
        self.start_date = date(2017, 1, 1)
        self.end_date = date(2019, 8, 21)
        self.current_date = self.start_date
        
        self.tracks = []
        self.session = requests.Session()

        return

    
    def connect_to_web_site(self):
        link = self.get_full_link()
        print("Connecting to " + link)
        page = self.session.get(link, verify = False)
        if page.status_code == 200:
            print("Connected")
            self.scrap_info_from_page(page.text)
        else:
            print("Unable to connect to " + link + ". Aborting...")
            sys.exit()
    
    def get_full_link(self):
        return self.base_link + self.country + "/" + self.frequency + "/" + str(self.current_date)
    
    def change_date(self):
        self.current_date = self.current_date + timedelta(days=1)
    
    def should_stop(self):
        return self.current_date == date(2017, 1, 7)
        # return self.current_date == self.end_date

    
    def scrap_info_from_page(self, page_text):
        beautiful_soup = BeautifulSoup(page_text, "html.parser")
        for track_component in beautiful_soup.find_all("tbody")[0].find_all("tr"):
            track_artist = track_component.find_all("td", {"class": "chart-table-track"})[0].find_all("span")[0].text
            track_name = track_component.find_all("td", {"class": "chart-table-track"})[0].find_all("strong")[0].text
            track_streams = int(track_component.find_all("td", {"class": "chart-table-streams"})[0].text.replace(",",""))
            track_link = track_component.find_all("td", {"class": "chart-table-image"})[0].find_all("a", href=True)[0]['href']
            track_image_link = track_component.find_all("td", {"class": "chart-table-image"})[0].find_all("a", href=True)[0].find_all("img")[0]['src']
            track_chart_position = int(track_component.find_all("td", {"class": "chart-table-position"})[0].text)

            new_track = Track(track_artist, track_name, track_streams, track_link, track_image_link, track_chart_position, True)

            # print(new_track.to_json())

            self.tracks.append(new_track.__dict__)
        
        self.write_file()
        self.change_date()
    
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



if __name__ == "__main__":
    print("Hello World")
    scrapper = Scrapper()
    while not scrapper.should_stop():
        scrapper.connect_to_web_site()