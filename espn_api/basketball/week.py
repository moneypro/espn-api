import datetime
from espn_api.basketball.league import League
from espn_api.basketball.constant import PRO_TEAM_MAP


class Week:

    scoring_period: (int, int)
    team_game_list: [[str]]

    def __init__(self, league: League, match_up_week: int):
        self.league = league
        self.scoring_period = self._match_up_week_to_scoring_period_convert(match_up_week)
        self.team_game_list = self._get_team_game_list()

    def _get_team_game_list(self):
        return [[PRO_TEAM_MAP[team_id] for team_id in self.league._get_pro_schedule(scoring_period).keys()] \
                for scoring_period in range(self.scoring_period[0], self.scoring_period[1] + 1)]

    @staticmethod
    def _match_up_week_to_scoring_period_convert(match_up_week: int) -> (int, int):
        """ Only works for year 2020-2021, return indices inclusive"""
        if match_up_week == 1:
            return 1, 6
        return 7 * (match_up_week - 1), 7 * match_up_week - 1

    def cumulate_number_of_games(self) -> dict[str, int]:
        number_of_games_for_team = dict()
        for game_day in self.team_game_list:
            for team_name in game_day:
                number_of_games_for_team[team_name] = number_of_games_for_team.get(team_name, 0) + 1
        return number_of_games_for_team

