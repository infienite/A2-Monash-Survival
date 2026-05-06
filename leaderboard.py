from campus import LeaderboardReader, Player
from algorithms import quick_sort
from data_structures import ArrayList

class Leaderboard:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        list_of_players: ArrayList[Player] = LeaderboardReader.read(campus_name)
        
        quick_sort.quick_sort(list_of_players, lambda p: (p.score, p.stamina))

        n = len(list_of_players)
        for i in range(len(list_of_players) // 2):
            temp = list_of_players[i]
            list_of_players[i] = list_of_players[n-i-1]
            list_of_players[n-i-1] = temp

        self.players = list_of_players

    def combine(self, other_leaderboard: Leaderboard):
        """
        Analyse your time complexity of this method.
        """
        combined_players = ArrayList(len(self.players) + len(other_leaderboard.players))

        i, j = 0, 0
        while i < len(self.players) and j < len(other_leaderboard.players):
            player_i = self.players[i]
            player_j = other_leaderboard.players[j]
            if player_j.score == player_i.score and player_j.stamina > player_i.stamina or player_j.score > player_i.score:
                combined_players.append(player_j)
                j += 1
            else:
                combined_players.append(player_i)
                i += 1
        
        while i < len(self.players):
            player_i = self.players[i]
            combined_players.append(player_i)
            i += 1

        while j < len(other_leaderboard.players):
            player_j = other_leaderboard.players[j]
            combined_players.append(player_j)
            j += 1
        
        self.players = combined_players
        
        for player in self.players:
            print(player)
        

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == "__main__":
    leaderboard = Leaderboard("clayton")
    other_leaderboard = Leaderboard("malaysia")

    leaderboard.combine(other_leaderboard)
    # Add test code here
