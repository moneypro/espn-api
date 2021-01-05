from espn_api.basketball import Player, League
from espn_api.basketball.constant import PRO_TEAM_MAP


class GameDayPlayerGetter:
    def __init__(self, league: League, roster: [Player]):
        self.roster = roster
        self.league = league

    def get_players_playing(self, scoring_period: int) -> [Player]:
        team_playing = self.get_games(scoring_period)
        return [player for player in self.roster if player.proTeam in team_playing]

    def get_games(self, scoring_period):
        return [PRO_TEAM_MAP[team_id] for team_id in self.league._get_pro_schedule(scoring_period).keys()]

    # def get_active_roster(self, scoring_period):
    #     "https://fantasy.espn.com/apis/v3/games/fba/seasons/2021/segments/0/leagues/30695?forTeamId=2&scoringPeriodId=16&view=mRoster"