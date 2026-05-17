from campus import LeaderboardReader, Player
from algorithms import merge_sort
from data_structures import ArrayList


def is_leaderboard_sorted(leaderboard: ArrayList[Player]) -> bool:
    """Checks whether the leaderboard is already sorted. Returns `True` if the leaderboard is sorted. Else, return `False`."""

    # Set the initial score and stamina as a very big number
    prev_score, prev_stamina = float("inf"), float("inf")

    # Checks loop invariant holds or not at each iteration
    for i in range(len(leaderboard)):

        # Get player score and stamina
        player_i = leaderboard[i]
        cur_score, cur_stamina = player_i.score, player_i.stamina

        # Loop invariant. The current score and stamina must be strictly less than or equal to the previous score and stamina.
        if cur_score <= prev_score and cur_stamina <= prev_stamina:

            # Keeps updating the value to compare next element with the current element
            prev_score = cur_score
            prev_stamina = cur_stamina

        else:
            # Loop invariant breached
            return False

    # All loop invariant fulfilled
    return True


class Leaderboard:
    def __init__(self, campus_name):
        """
        Best case time complexity is O(N) where N is the length of the list.
        Best case happens when the leaderboard is already sorted in descending order based on
        score and stamina. The is_leaderboard_sorted will check if the leaderboard is already
        sorted in the correct order. When the leaderboard is sorted, it will halt early. Thus,
        elements are iterated N times to check the sorted status and halts.

        Worst case time complexity is O(N log N) where N is the length of the list.
        Worst case happens when the leaderboard undergoes mergesort operation. The list will
        be divided by half until each partition becomes pair of 2 elements. This takes about
        O(N log N) as the length of the list is divided by 2 each iteration and in each
        iteration, all N elements are visited to be copied into a new, smaller array. The merge
        operation takes O(N) time as in each iteration, the each element of the array
        will be merged into a bigger array. As the array length starts expanding by a factor of
        2 as more elements merge, the final array can be achieved in O(log N) steps of
        iteration. So, it takes O(N log N) as well.
        """
        # Get leaderboard data
        self.players: ArrayList[Player] = LeaderboardReader.read(campus_name)

        # Checks whether the leaderboard is already sorted
        if is_leaderboard_sorted(self.players):
            return

        # Sort in descending order based on score and stamina in descending order
        self.players = merge_sort.merge_sort(
            self.players, lambda p: (-p.score, -p.stamina)
        )

    def combine(self, other_leaderboard: Leaderboard):
        """
        Best and worst case time complexity is O(N) where N = length of current leaderboard +
        length of other leaderboard.
        Best and worst case happens when both leaderboard lists are sorted descendingly from the
        player with the highest score and stamina to the lowest. Each element is only visited
        once and added to the final list which contains the combined leaderboard in descending
        order.
        """
        # Merge two leaderboards in descending order prioritizing the first list items for equal keys of the first and second list
        self.players = merge_sort.merge(
            self.players, other_leaderboard.players, lambda p: (-p.score, -p.stamina)
        )

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
    # for player in leaderboard.players:
    #     print(player)

    # ids = [4,7,2,10,8,3,1,6,9,5]
    # for i in range(len(leaderboard.players)):
    #     assert ids[i] == leaderboard.players[i].id

    # other_leaderboard = Leaderboard("malaysia")
    # # print(other_leaderboard.players)
    # ids = [20,17,12,16,14,11,18,13,19,15]
    # for i in range(len(other_leaderboard.players)):
    #     assert ids[i] == other_leaderboard.players[i].id

    # leaderboard.combine(other_leaderboard)
    # for player in leaderboard.players:
    #     print(player)

    # ids = [4, 7, 2, 20, 17, 12,10,16,8,14,11,3,18,1,6,13,9,19,15,5]
    # for i in range(len(leaderboard.players)):
    #     assert ids[i] == leaderboard.players[i].id
