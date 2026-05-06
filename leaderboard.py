from campus import LeaderboardReader

class Leaderboard:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        list_of_players = LeaderboardReader.read(campus_name)
        pass

    def combine(self, other_leaderboard):
        """
        Analyse your time complexity of this method.
        """
        pass

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == "__main__":
    leaderboard = Leaderboard("clayton")
    # Add test code here
