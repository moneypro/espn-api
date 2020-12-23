from espn_api.basketball import Player, League
from espn_api.basketball.constant import PRO_TEAM_MAP


# TODO: Consider the case where the roster is full, i.e. no more 10 players a day, also consider positions, injury status
def predict(roster: list[Player], number_of_games_map: dict[str, int]) -> (int, int):
    lo = 0
    hi = 0
    for player in roster:
        lo_stats, hi_stats = get_lo_hi_stats(player)
        number_of_games_this_period = number_of_games_map.get(player.proTeam, 0)
        lo += number_of_games_this_period * lo_stats
        hi += number_of_games_this_period * hi_stats
    return lo, hi


def get_lo_hi_stats(player: Player) -> (int, int):
    projected_season_stat = get_fantasy_pts(player.stats['102021']['avg'])
    if '002020' not in player.stats:
        return projected_season_stat, projected_season_stat
    past_season_stat = get_fantasy_pts(player.stats['002020']['avg'])
    return min(past_season_stat, projected_season_stat), max(past_season_stat, projected_season_stat)


def cumulate_number_of_games(match_up_week: int, league: League) -> dict[str, int]:
    number_of_games_for_team = dict()
    scoring_period_lo, scoring_period_hi = match_up_week_to_scoring_period_convert(match_up_week)
    for scoring_period in range(scoring_period_lo, scoring_period_hi + 1):
        for team_id in league._get_pro_schedule(scoring_period).keys():
            number_of_games_for_team[PRO_TEAM_MAP[team_id]] = number_of_games_for_team.get(PRO_TEAM_MAP[team_id], 0) + 1
    return number_of_games_for_team

'''
 'BLK': 1.0175438596491229,
   'STL': 1.0350877192982457,
   'AST': 5.771929824561403,
   'OREB': 2.280701754385965,
   'DREB': 11.456140350877194,
   'REB': 13.736842105263158,
   'PF': 3.0350877192982457,
   'TO': 3.6666666666666665,
   'FGM': 10.929824561403509,
   'FGA': 19.982456140350877,
   'FTM': 6.333333333333333,
   'FTA': 10.0,
   '3PTM': 1.456140350877193,
   '3PTA': 4.754385964912281,
   'FG%': 0.54697103,
   'FT%': 0.63333333,
   '3PT%': 0.30627306,
   'MPG': 30.9122807,
   'MIN': 30.912280701754387,
   'GP': 1.0},
'''


def get_fantasy_pts(stats: dict) -> float:
    return get_stat(stats, 'PTS') + get_stat(stats, '3PTM') - stats['FGA'] + stats['FGM'] * 2 - stats['FTA'] + stats['FTM'] \
           + stats['REB'] + stats['AST'] * 2 + stats['STL'] * 4 + stats['BLK'] * 4 - stats['TO'] * 2


def get_stat(stats: dict, key: str) -> float:
    if key in stats:
        return stats[key]
    return 0


def match_up_week_to_scoring_period_convert(match_up_week: int) -> (int, int):
    """ Only works for year 2020-2021, return indices inclusive"""
    if match_up_week == 1:
        return 1, 6
    return 7 * (match_up_week - 1), 7 * match_up_week - 1
