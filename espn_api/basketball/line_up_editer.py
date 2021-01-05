from .league import League

'''
{"isLeagueManager":false,"teamId":2,"type":"ROSTER","memberId":"{3C4A75B6-F84B-48AE-8A75-B6F84B48AE47}","scoringPeriodId":7,"executionType":"EXECUTE","items":[{"playerId":4277905,"type":"LINEUP","fromLineupSlotId":0,"toLineupSlotId":11},{"playerId":4066636,"type":"LINEUP","fromLineupSlotId":11,"toLineupSlotId":0}]}
Line up slot:
PG: 0,
SG: 1,
SF: 2,
PF: 3,
C: 4,
UTIL: 11.
'''


class LineUpEditor:

    def __init__(self, league: League, team_id: int):
        self.league = league
        self.team_id = team_id
        self.swid = self.league.espn_request.cookies['SWID']
        self.roster = self.league.get_team_data(self.team_id).roster

    def change_line_up(self, payload):
        data = self.league.espn_request.league_post(payload=payload, extend="/transactions/")
        return data

    def bench_all_players(self, scoring_period):
        """
        This breaks if you have someone on the current roster but you have already dropped. i.e. inconsistency between current roster and future roster
        """

        for player in self.roster:
            move_to_bench_command = [
                {"playerId": player.playerId, "type": "LINEUP", "fromLineupSlotId": 0, "toLineupSlotId": 12}]
            payload = {"isLeagueManager": "false", "teamId": self.team_id, "type": "FUTURE_ROSTER", "memberId": self.swid,
                       "scoringPeriodId": scoring_period, "executionType": "EXECUTE",
                       "items": move_to_bench_command}
            self.change_line_up(payload)

    def fill_line_up(self, scoring_period, sort_stats_by='002021'):
        """
        Undefined behavior for active player > 10. TODO: Manage by avg stats.
        """