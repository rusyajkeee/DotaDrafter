import constants

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

def sort_by_winrate(matchups):
    return sorted(matchups, key=lambda x: x["winRate"], reverse=True)

def print_best_matchups(matchups, heroid, top_n=5):
    print(f"Top {top_n} Matchups for {constants.HEROES.get(heroid, 'Unknown Hero')}:")
    for matchup in matchups[:top_n]:
        print(f"{matchup['heroName']}: {matchup['winRate']}% win rate over {matchup['matchCount']} matches")

def print_worst_matchups(matchups, heroid, top_n=5):
    print(f"Worst {top_n} Matchups for {constants.HEROES.get(heroid, 'Unknown Hero')}:")
    for matchup in range(len(matchups) - 1, len(matchups) - top_n - 1, -1):
        print(f"{matchups[matchup]['heroName']}: {matchups[matchup]['winRate']}% win rate over {matchups[matchup]['matchCount']} matches")