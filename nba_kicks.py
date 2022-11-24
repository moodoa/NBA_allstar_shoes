import json
import time
import requests
from bs4 import BeautifulSoup
from random import randint

class NBAKICKS:

    def get_allstar_player(self):
        with open("./allstar.json", "r") as file:
            data = json.load(file)
        return data[str(randint(0, 286))]

    def get_player_info_url(self, player):
        player = player.lower().replace(" ", "")
        text = requests.get("https://kixstats.com/players").text
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.select("div.player-name"):
            if tag.a.string.strip().lower().replace(" ", "") == player:
                return tag.a["href"]
        return False

    def get_player_shoes(self, url):
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")
        shoes = soup.select("span.player-brand-h")
        return shoes[randint(0, len(shoes)-1)].text

    def get_your_shoes(self):
        url = False
        while not url:
            player = self.get_allstar_player()
            url = self.get_player_info_url(player)
        shoes = self.get_player_shoes(url)
        res = f"Your allstar player is {player}, and his shoes are {shoes}!"
        return res
        
if __name__ == "__main__":
    kicks = NBAKICKS()
    print("ready?")
    time.sleep(.5)
    print("3")
    res = kicks.get_your_shoes()
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(.5)
    print(res)