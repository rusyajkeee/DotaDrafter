import cache
import constants
import stratz_api
import matchup_utils
import recommender

cache_data = cache.load_cache()

print(recommender.recommend(cache_data, [10], "POSITION_1", [10], 20))