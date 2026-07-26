from pathlib import Path
import json
from constants import HEROES
import stratz_api
import matchup_utils
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
now = datetime.now().isoformat()

CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "cache.json"

def load_cache():
    if CACHE_FILE.is_file():
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

        if datetime.fromisoformat(cache["created_at"]) < (datetime.now() - timedelta(hours=24)):
            return build_cache(version=cache["version"] + 1)

        cache = normalize_cache(cache)
        
        return cache

    return build_cache()

def normalize_cache(cache: dict) -> dict:
    cache["heroes"] = {
        int(hero_id): {
            **hero_data,
            "coefficients": {
                int(counter_id): coefficient
                for counter_id, coefficient in hero_data["coefficients"].items()
            }
        }
        for hero_id, hero_data in cache["heroes"].items()
    }


    
    return cache


def save_cache(cache):
    CACHE_DIR.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4, ensure_ascii=False)

def build_one_hero(hero_id):
    matchups = stratz_api.get_matchups(hero_id)
    matchups = matchup_utils.add_winrates(matchups)
    matchups = matchup_utils.sort_by_winrate(matchups)
    coefficients = matchup_utils.build_coefficients(matchups)
    return hero_id, coefficients



def build_cache(version: int = 1):

    cache = {"version": version, "created_at": datetime.now().isoformat(), "heroes": {}}
    positions = stratz_api.get_all_positions_stats()
    positions = matchup_utils.normalise_positions(positions)

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = {
        executor.submit(build_one_hero, hero_id): hero_id for hero_id in HEROES
        }

        completed = 0
        for future in as_completed(futures):
            hero_id = futures[future]
            try:
                hero_id, matchups =future.result()
                    
            except Exception as e:
                print(f"Error processing hero {HEROES[hero_id]}: {e}")
            else:
                cache["heroes"][str(hero_id)] = {
                "coefficients": matchups,
                "positions": positions[hero_id]
                }
                completed += 1

                print(f"[{completed}/{len(HEROES)}] {HEROES[hero_id]} processed successfully.")
    
    save_cache(cache)
    return cache

import time

start = time.perf_counter()

cache = load_cache()

print(f"Finished in {time.perf_counter() - start:.2f} seconds.")