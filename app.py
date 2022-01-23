import requests
from bs4 import BeautifulSoup
import time 
import pandas as pd

base_url = "https://kicks-online.net/en/ranking/global?pageno"
player_data = []

def map_row_to_player_data(row):
    '''
    Maps the tablerow HTML-element to player data

    Args:
        row: BeautifulSoup-component that represents the TR-element.

    Returns:
        Player-object
    '''
    try:
        player = {}
        player["id"] = row[1].a["data-id"]
        player["rank"] = row[0].text
        player["name"] = row[1].a.text
        player["position_id"] = row[2].span.text
        player["position_name"] = str(row[2].img["src"]).split("/")[-1].split(".")[0]
        player["level"] = int(row[3].text)
    except:
        return {}
    return player

def append_result_from_page_index(index:int):
    '''
    Appends all player data from a given index of the rankingtable

    Args:
        index: Integer that represent the index of the rankingtable
    '''
    resp = requests.get(f"{base_url}={index}").content
    bs_page = BeautifulSoup(resp, "lxml")

    table = bs_page.find("tbody",{"id":"rank_table"})
    for tr in table.find_all("tr"):
        temp_data = []
        for td in tr.find_all("td"):
            temp_data.append(td)
        player_data.append(map_row_to_player_data(temp_data))

def main():
    data = [*map(append_result_from_page_index, range(1,166))]
    print(player_data)
    print("Exporting data..")
    pd.DataFrame(player_data).to_csv("player_data.csv")
    print("File created!")


if __name__ == "__main__":
    main()