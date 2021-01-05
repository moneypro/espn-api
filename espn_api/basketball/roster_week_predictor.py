from espn_api.basketball.player import Player
from espn_api.basketball.week import Week


class RosterWeekPredictor:
    roster: [Player]
    week: Week

    def __init__(self, roster, week):
        self.roster = roster
        self.week = week

    def players_with_game(self, day: int) -> [Player]:
        team_playing = self.week.team_game_list[day]
        return [player for player in self.roster if player.proTeam in team_playing]

    def predict(self, daily_active_size=10) -> (int, int):
        lo = 0
        hi = 0
        for day in range(0, self.week.scoring_period[1] - self.week.scoring_period[0]):
            players_with_game = self.players_with_game(day)
            daily_lo = []
            daily_hi = []
            for player in players_with_game:
                if player.injuryStatus == 'ACTIVE':
                    lo_stats, hi_stats = self.get_lo_hi_stats(player)
                    daily_lo.append(lo_stats)
                    daily_hi.append(hi_stats)
            daily_hi.sort(reverse=True)
            daily_lo.sort(reverse=True)
            lo += sum(daily_lo[:min(len(daily_lo), daily_active_size)])
            hi += sum(daily_hi[:min(len(daily_hi), daily_active_size)])
        return lo, hi

    def get_total_number_of_games(self, daily_active_size=10) -> int:
        total = 0
        for day in range(0, self.week.scoring_period[1] - self.week.scoring_period[0]):
            players_with_game = self.players_with_game(day)
            healthy_players = [player for player in players_with_game if player.injuryStatus == 'ACTIVE']
            total += min(len(healthy_players), daily_active_size)
        return total

    @staticmethod
    def get_lo_hi_stats(player: Player) -> (int, int):
        stat_period_list = ['012021', '022021', '002021', '032021']
        fpts_for_stat_period = [RosterWeekPredictor.get_stat_from_stat_period(player, stat_period) for stat_period in stat_period_list]
        ignore_none_fpts_list = [fpts for fpts in fpts_for_stat_period if fpts is not None]
        return min(ignore_none_fpts_list), max(ignore_none_fpts_list)

    @staticmethod
    def get_stat_from_stat_period(player: Player, stat_period: str):
        if stat_period not in player.stats:
            return None
        return RosterWeekPredictor.get_fantasy_pts(player.stats[stat_period]['avg'])

    @staticmethod
    def get_fantasy_pts(stats: dict) -> float:
        return RosterWeekPredictor.get_stat_in_category(stats, 'PTS') + RosterWeekPredictor.get_stat_in_category(stats, '3PTM') - stats['FGA'] + stats[
            'FGM'] * 2 - stats['FTA'] + stats['FTM'] \
               + stats['REB'] + stats['AST'] * 2 + stats['STL'] * 4 + stats['BLK'] * 4 - stats['TO'] * 2

    @staticmethod
    def get_stat_in_category(stats: dict, cat: str) -> float:
        if cat in stats:
            return stats[cat]
        return 0
