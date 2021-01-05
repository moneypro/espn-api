from .constant import POSITION_MAP
from .league import League
from .player import Player
from .game_day_player_getter import GameDayPlayerGetter

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
        self.game_day_player_getter = GameDayPlayerGetter(league, self.roster)

    def change_line_up(self, payload):
        data = self.league.espn_request.league_post(payload=payload, extend="/transactions/")
        return data

    def bench_all_players(self, scoring_period):
        """
        This breaks if you have someone on the current roster but you have already dropped. i.e. inconsistency between current roster and future roster
        """
        bench_slot_id = POSITION_MAP['BE']
        # TODO: See below. Also, ignore IR player.
        for player in self.roster:
            move_to_bench_command = [
                {"playerId": player.playerId, "type": "LINEUP", "toLineupSlotId": bench_slot_id}]
            payload = {"isLeagueManager": "false", "teamId": self.team_id, "type": "FUTURE_ROSTER", "memberId": self.swid,
                       "scoringPeriodId": scoring_period, "executionType": "EXECUTE",
                       "items": move_to_bench_command}
            try:
                self.change_line_up(payload)
            except:
                print("Failed to bench player ", player)

    def fill_line_up(self, scoring_period, sort_stats_by='002021'):
        """
        Undefined behavior for active player > 10. TODO: Manage by avg stats.
        """
        self.bench_all_players(scoring_period)
        players_playing_that_day = self.game_day_player_getter.get_players_playing(scoring_period)
        line_up = self.get_optimized_line_up(players_playing_that_day)
        for player_id, to_line_up_slot_id in line_up:
            move_command = [
                {"playerId": player_id, "type": "LINEUP", "toLineupSlotId": to_line_up_slot_id} ]
            payload = {"isLeagueManager": "false", "teamId": self.team_id, "type": "FUTURE_ROSTER", "memberId": self.swid,
                       "scoringPeriodId": scoring_period, "executionType": "EXECUTE",
                       "items": move_command}
            # TODO: Use one single request and get the roster of that day.
            # 如果你当前名单和未来名单不一样
            # 而且那一天当前名单多出来的人又有比赛的话会报错
            #  "https://fantasy.espn.com/apis/v3/games/fba/seasons/2021/segments/0/leagues/30695?forTeamId=2&scoringPeriodId=16&view=mRoster"
            try:
                self.change_line_up(payload)
            except:
                print("Failed to change line up for player ", player_id)

    def get_optimized_line_up(self, active_players: [Player], sort_stats_by='002021') -> [(str, int)]:
        """
        Return list of tuple (player id, to line up slot id).
        This currently only supports when your line up is of PG, SG, SF, PF, C and 5 UTILs.
        """
        fixed_slots = {}
        util_list = []
        assigned_player_id_set = set()
        # TODO: Say I don't have any pure SF, but Tatum is SF, PF, he doesn't get filled into SF directly
        for player in active_players:
            positions = LineUpEditor.get_available_position(player.eligibleSlots)
            if len(positions) == 1 and positions[0] not in fixed_slots: # single position, put into the slot
                assigned_player_id_set.add(player.playerId)
                fixed_slots[positions[0]] = player.playerId
            elif len(assigned_player_id_set) < 10 and len(util_list) < 5:
                assigned_player_id_set.add(player.playerId)
                util_list.append(player.playerId)
        line_up = []
        [line_up.append((playerId, POSITION_MAP[position])) for position, playerId in fixed_slots.items()]
        [line_up.append((playerId, POSITION_MAP['UT'])) for playerId in util_list]
        return line_up

    @staticmethod
    def get_available_position(eligible_slots: [str]):
        # PG, SG, SF, PF, C
        available_positions = [POSITION_MAP[i] for i in range(5)]
        return [eligible_slot for eligible_slot in eligible_slots if eligible_slot in available_positions]

