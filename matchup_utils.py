import constants
from math import log10

COEFFICIENTS = [
    100, 95, 90, 85, 80,
    76, 72, 68, 64, 60,
    56, 52, 48, 44, 40,
    36, 32, 28, 24, 20,
    18, 16, 14, 12, 10,
    8, 6, 4, 2, 1
]


def add_winrates(matchups):
    new_matchups = []
    for matchup in matchups:
        new_matchup = matchup.copy()
        new_matchup["winRate"] = round((matchup["winCount"] / matchup["matchCount"] * 100), 2) if matchup["matchCount"] > 0 else 0
        new_matchups.append(new_matchup)
    return new_matchups


def add_hero_names(matchups: list[dict], heroes: dict[int, str]) -> list[dict]:
    matchups_with_names = []
    for matchup in matchups:
        matchup_with_name = matchup.copy()
        matchup_with_name["heroName"] = heroes.get(matchup_with_name["heroId2"], "Unknown Hero")
        matchups_with_names.append(matchup_with_name)
    return matchups_with_names


def normalise_positions(positions_stats):
    normalised_positions = {}
    
    for hero in positions_stats:
        normalised_positions.setdefault(hero, {})
        total_matches = 0
        for position in constants.POSITIONS:
            total_matches += positions_stats[hero][position]["matchCount"]
        for position in constants.POSITIONS:
            if total_matches != 0:
                normalised_positions[hero][position] = round(positions_stats[hero][position]["matchCount"] / total_matches, 3)
            else:
                normalised_positions[hero][position] = 0
    return normalised_positions


def sort_by_winrate(matchups):
    return sorted(matchups, key=lambda x: x["winRate"], reverse=False)


import math
def build_coefficients(
    matchups: list[dict],
    unavailable_heroes: list[int] | None = None
) -> dict[int, int]:

    if unavailable_heroes is None:
        unavailable_heroes = []

    filtered = [
        matchup
        for matchup in matchups
        if matchup["heroId2"] not in unavailable_heroes
    ][:30]

    coefficients = {}

    for rank, matchup in enumerate(filtered):
        match_count = matchup["matchCount"]

        multiplier = min(1.15, 0.85 + math.log10(match_count) / 10)
        coefficient = COEFFICIENTS[rank] * multiplier

        coefficients[matchup["heroId2"]] = coefficient

    return coefficients


def print_best_matchups(matchups, heroid, top_n=5):
    print(f"Top {top_n} Matchups for {constants.HEROES.get(heroid, 'Unknown Hero')}:")
    for matchup in matchups[:top_n]:
        print(f"{matchup['heroName']}: {matchup['winRate']}% win rate over {matchup['matchCount']} matches")


def print_worst_matchups(matchups, heroid, top_n=5):
    print(f"Worst {top_n} Matchups for {constants.HEROES.get(heroid, 'Unknown Hero')}:")
    for matchup in range(len(matchups) - 1, len(matchups) - top_n - 1, -1):
        print(f"{matchups[matchup]['heroName']}: {matchups[matchup]['winRate']}% win rate over {matchups[matchup]['matchCount']} matches")

