import requests
import constants
from dotenv import load_dotenv
import os
from matchup_utils import add_hero_names, add_winrates, print_best_matchups, print_worst_matchups, sort_by_winrate
from time import sleep

HEROES = constants.HEROES
load_dotenv()

TOKEN = os.getenv("STRATZ_TOKEN")
URL = "https://api.stratz.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def execute_query(query: str) -> dict:
    response = requests.post(
        URL,
        json={"query": query},
        headers=HEADERS
    )

    if response.status_code == 429:
            sleep(1)
            return execute_query(query)
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    if "errors" in data or "data" not in data:
        raise Exception(f"Query failed with errors: {data.get('errors')}")
    
    return data["data"]

def get_matchups(hero_id: int):
    query = f"""
query MyQuery {{
  heroStats {{
    matchUp(heroId: {hero_id} take: 200) {{
      vs {{
        heroId2
        matchCount
        winCount
      }}
    }}
  }}
}}
"""
    return execute_query(query)["heroStats"]["matchUp"][0]["vs"]


#print(sort_by_winrate(add_hero_names(add_winrates(get_matchups(1)), HEROES)))
