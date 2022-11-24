import json
import requests
from bs4 import BeautifulSoup
from random import randint, choices


class NBAKICKS:
    def get_allstar_player(self):
        with open("./allstar_players.json", "r") as file:
            data = json.load(file)
        return data

    def get_starter_five(self):
        all_players = self.get_allstar_player()
        guard = []
        forward = []
        center = []
        guard = self._select_players(guard, "g", 2, all_players)
        forward = self._select_players(forward, "f", 2, all_players)
        center = self._select_players(center, "c", 1, all_players)
        starters = guard + forward + center
        return starters

    def _select_players(self, position, pos_name, pos_need, all_players):
        while len(position) < pos_need:
            positions = choices(all_players[pos_name], k=10)
            for p in positions:
                if p not in position:
                    position.append(p)
                    if len(position) == pos_need:
                        break
        return position

    def get_player_info_url(self, player):
        player_info = {}
        player_name = player.lower().replace(" ", "").replace("ć", "c").replace("č", "c")
        text = requests.get("https://kixstats.com/players").text
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.select("div.player-name"):
            if tag.a.string.strip().lower().replace(" ", "") == player_name:
                player_info[player] = tag.a["href"]
        return player_info

    def get_player_shoes(self, player_info):
        players_shoes = {}
        for player, url in player_info.items():
            text = requests.get(url).text
            soup = BeautifulSoup(text, "html.parser")
            shoes = soup.select("span.player-brand-h")
            players_shoes[player] = shoes[randint(0, len(shoes) - 1)].text
        return players_shoes

    def get_your_shoes(self):
        print("Your All Star Players Shoes Are:\n")
        starters = self.get_starter_five()
        for starter in starters:
            player_info = self.get_player_info_url(starter)
            player_shoes = self.get_player_shoes(player_info)
            print(f"{list(player_shoes.values())[0]} ({list(player_shoes.keys())[0]})")
            print("\n")
        return ""


if __name__ == "__main__":
    kicks = NBAKICKS()
    res = kicks.get_your_shoes()
