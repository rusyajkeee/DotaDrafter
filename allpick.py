import stratz_api
import matchup_utils
import constants

"""
All Pick functionality

1. Get all enemy hero IDs.

2. Fetch matchup data for every enemy hero.

3. Calculate win rates.

4. Sort every matchup list by ascending win rate.

5. Assign coefficient points based on matchup rank.

6. Merge coefficient tables from all enemy heroes.

7. Remove:
   - picked heroes
   - banned heroes
   - unavailable heroes

8. Sort by total score.

9. Print Top-N recommendations.
"""