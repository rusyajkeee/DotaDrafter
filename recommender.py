import constants
def calculate_scores(
    cache: dict,
    enemy_heroes: list[int],
    position: str,
    unavailable_heroes: list[int] | None = None,
    
) -> dict[int, float]:
    
    if unavailable_heroes is None:
        unavailable_heroes = []
    scores = merge_enemy_coefficients(cache, enemy_heroes)
    scores = remove_unavailable(scores, unavailable_heroes)
    scores = apply_position_weights(scores, cache, position)
    return scores


def merge_enemy_coefficients(
    cache: dict,
    enemy_heroes: list[int]
) -> dict[int, float]:
    scores = {}
    for enemy in enemy_heroes:
        hero_coefficients = cache["heroes"][enemy]["coefficients"]
        for hero_id, coefficient in hero_coefficients.items():
            scores[hero_id] = scores.get(hero_id, 0) + coefficient
    return scores

def remove_unavailable(
    scores: dict[int, float],
    unavailable_heroes: list[int]
) -> dict[int, float]:
    for hero in unavailable_heroes:
        scores.pop(hero, None)
        
    return scores

def position_multiplier(weight: float) -> float:
    return weight ** 2

def apply_position_weights(
    scores: dict[int, float],
    cache: dict,
    position: str | None
) -> dict[int, float]:
    if position is None:
        return scores
    for hero_id in scores:
        weight = cache["heroes"][hero_id]["positions"][position]
        scores[hero_id] *= position_multiplier(weight)
    return scores


def apply_ally_synergy():
    #Synergies with teammates. Synergies can be get from in STRATZ API
    pass

def apply_comfort_bonus():
    #Comfort for player. Need to analyse player's stats
    pass

def recommend(
    cache: dict,
    enemy_heroes: list[int],
    position: str,
    unavailable_heroes: list[int] | None = None,
    top_n = 5 
    ) -> dict[int, float]:
        scores = calculate_scores(cache, enemy_heroes, position, unavailable_heroes)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return format_recommendations(sorted_scores[:top_n])


def format_recommendations(scores):
    new_recommendation = []
    for hero_id, hero_score in scores:
        new_recommendation.append({
        "heroId": hero_id,
        "heroName": constants.HEROES[hero_id],
        "score": hero_score
        })
    return new_recommendation

def print_recommendations(scores):
    i = 1
    for score in scores:
        print(f"{i}.{constants.HEROES[score[0]]}")
        i+=1

