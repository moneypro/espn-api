from espn_api.basketball import League, Matchup, Team
import logging

# Init logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

espn_s2 = "AECc%2BKMx5L8l9Rai5PHG%2FT%2Fjtw%2BR%2FZozX391uxpta1J6tD61%2F4NV88%2BVPlCSe0Wjcg0J9jJ0oTJ%2BMkehJLT8MSDfgiubWB9F1n3H%2BnTHWc9OTkzM2ceQFGPiA%2B9AF4yQzt0I3%2FdCgk%2BdQLbgybhS6y1yRS9NIDyfXMSgcqFqRbn5F7zBTzwu9A%2BD2Pi6g6KMR29PbmNbtxSrCJkfbF%2BaZtrpqDbHBZhLyfqOAhQIDx0q1iD0u1DkhxVNoRnxx%2FmEvS%2FHEJZWmfvZM%2F0IAHxPrfVx"
league = League(league_id=30695, year=2021, espn_s2=espn_s2, swid="{3C4A75B6-F84B-48AE-8A75-B6F84B48AE47}")
logger.info(league.get_team_data(2).schedule[0].away_team)
