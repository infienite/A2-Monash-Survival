from campus import LeaderboardReader, Player
from algorithms import quick_sort, merge_sort
from data_structures import ArrayList, LinkedList, LinkedStack, ArrayR, LinkedQueue

class Leaderboard:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        list_of_players: ArrayList[Player] = LeaderboardReader.read(campus_name)
        
        list_of_players = merge_sort.merge_sort(list_of_players, lambda p: (p.score, p.stamina))

        n = len(list_of_players)
        desc = ArrayList(n)
        queue = LinkedStack()
        queue.push(list_of_players[-1])
        for i in range(1, n):
            p: Player = list_of_players[n-i-1]
            prev_p: Player = queue.peek()
            if (p.score, p.stamina) != (prev_p.score, prev_p.stamina):
                while not queue.is_empty():
                    desc.append(queue.pop())
            queue.push(p)
        while not queue.is_empty():
            desc.append(queue.pop())

        self.players = desc

    def combine(self, other_leaderboard: Leaderboard):
        """
        Analyse your time complexity of this method.
        """
        self.players = merge_sort.merge(self.players, other_leaderboard.players, lambda p: (-p.score, -p.stamina))


    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == "__main__":

    # arr_test = ArrayList(5)
    # arr_test.append(("A", 1, 4))
    # arr_test.append(("B", 2, 5))
    # arr_test.append(("C", 2, 5))
    # arr_test.append(("D", 2, 6))
    # arr_test.append(("E", 1, 3))

    # arr_test = merge_sort.merge_sort(arr_test, lambda x: (x[1], x[2]))

    # for n in arr_test:
    #     print(n)

    # exit(0)

    leaderboard = Leaderboard("clayton")
    for player in leaderboard.players:
        print(player)
    other_leaderboard = Leaderboard("malaysia")
    print(other_leaderboard.players)

    leaderboard.combine(other_leaderboard)
    for player in leaderboard.players:
        print(player)
    # Add test code here
