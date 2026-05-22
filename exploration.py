from campus import Campus, Location, Connection
from data_structures import LinkedList


def validate_location_arg(location: Location):
    """Validate `location` argument. `location` must be of type Location."""
    if location == None:
        raise ValueError("location argument cannot be None")
    if type(location) != Location:
        raise ValueError("location argument must be of Location type")


def validate_stamina_arg(stamina: int):
    """Validate `stamina` argument. `stamina` must be a positive integer and `stamina > 0`."""
    if type(stamina) != int or stamina <= 0:
        raise ValueError("stamina argument must be a non-zero positive integer")


class Exploration:
    def __init__(self, campus_name):
        self.campus = Campus(campus_name)

    def greedy_student(self, location: Location, stamina: int):
        """
        Best case time complexity is O(1).
        Best case happens when the first location has 0 connection to other locations. In this case,
        the function run once and halts regardless of the number of stamina of the student.

        Worst case time complexity is O(N+C), where N is the number of location visited until the
        stamina finishes or until a location with 0 connection to other locations. C is the total
        number of connections outgoing from all locations visited.
        Worst case happens when there are N locations which contains connection to other location
        bounded by the number of stamina. At each location starting from the first location, Ci
        connections are evaluated where i represents the node number and Ci represents the number
        of connections outgoing from node i. Each connection is evaluated in order to find the
        next location which has the lowest difficulty and highest reward. This process repeats for
        N locations until the stamina reaches 0 or the function reaches a location which have 0
        connection to other locations. As a result, the function takes O(N) time to visit each
        location and at each location takes O(Ci) time to evaluate each connection. In total,
        C1 + C2 + ... + Ci is equal to C. Therefore, the function takes O(N+C) time to complete.
        """

        # Validate arguments
        validate_location_arg(location)
        validate_stamina_arg(stamina)

        def greedy_student_aux(cur_location: Location, cur_stamina: int):
            """Calculate the highest rewards obtained when each locations are visited in order of lowest path difficulty and highest location reward bound by the number of stamina."""
            # Get all connections from this location
            conns: LinkedList[Connection] = cur_location.get_connections()

            # Base case. When stamina is 0 or when the location has no connection to other location
            if cur_stamina <= 0 or len(conns) == 0:

                # Yields the location reward
                return cur_location.get_reward()

            # Remove first item of the list as the default value for comparison
            temp: Connection = conns.delete_at_index(0)
            next_conn: Connection = temp

            # Finds the connection which has the lowest difficulty and highest reward
            for conn in conns:
                if (
                    conn.get_difficulty() == next_conn.get_difficulty()
                    and conn.get_location().get_reward()
                    > next_conn.get_location().get_reward()
                    or conn.get_difficulty() < next_conn.get_difficulty()
                ):
                    next_conn = conn

            # Reinsert the first item
            conns.insert(0, temp)

            # Yield = current location reward + sum of location reward of next location until the final location
            return cur_location.get_reward() + greedy_student_aux(
                next_conn.get_location(), cur_stamina - 1
            )

        # The auxiliary function does the recursive calls and computations
        return greedy_student_aux(location, stamina)

    def total_difficulty(self, location: Location):
        """
        Time complexity analysis not required for this method.
        """
        # Validate argument
        validate_location_arg(location)

        def total_difficulty_aux(location: Location, accumulated_difficulty: int):
            """Calculate the total difficulty across all possible paths starting from `location` given. Use the `accumulated_difficulty` to track total difficulty accumulated before a location is visited."""
            # Get all connections from this location
            conns = location.get_connections()

            # Base case. When the location has no connection
            if len(conns) == 0:
                return accumulated_difficulty

            # Calculate the sum of difficulty of for each possible path starting at each connections
            total_diff = 0
            for conn in conns:
                # Total difficulty of connection = difficulty of connection + total difficulty of next connection
                total_diff += total_difficulty_aux(
                    conn.get_location(), accumulated_difficulty + conn.get_difficulty()
                )

            # Yield sum of difficulty
            return total_diff

        # The auxiliary function does the recursive calls and computations
        return total_difficulty_aux(location, 0)

    def total_reward_for_longest_path(self, location: Location):
        """
        Time complexity analysis not required for this method.
        """
        # Validate argument
        validate_location_arg(location)

        def total_reward_for_longest_path_aux(
            location: Location, length: int, total_reward: int = 0
        ):
            """Calculate the total reward for the longest path."""
            # Get all connections from this location
            conns = location.get_connections()

            # Base case. When the location has no connection
            if len(conns) == 0:
                return (length, total_reward + location.get_reward())

            # Remove first item of the list as the default value for comparison
            temp: Connection = conns.delete_at_index(0)
            max_length, max_reward = total_reward_for_longest_path_aux(
                temp.get_location(), length + 1, total_reward + location.get_reward()
            )

            # Finds the connection which will yield the longest path which gets the highest reward
            for conn in conns:

                # Connection with longest path and highest reward = (current path length + 1, total reward + current location reward)
                cur_length, cur_reward = total_reward_for_longest_path_aux(
                    conn.get_location(),
                    length + 1,
                    total_reward + location.get_reward(),
                )

                # The connection with longest path is chosen regardless of the reward but higher reward is chosen when equal the longest path
                if (
                    cur_length == max_length
                    and cur_reward > max_reward
                    or cur_length > max_length
                ):
                    max_length = cur_length
                    max_reward = cur_reward

            # Reinsert the first item
            conns.insert(0, temp)

            # Return the longest path length and highest reward
            return (max_length, max_reward)

        # The auxiliary function does the recursive calls and computations. Only return the max reward, longest path is only used inside the recursive function for computation
        return total_reward_for_longest_path_aux(location, 1)[1]

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == "__main__":

    clayton = Exploration("clayton")
    # print(clayton.greedy_student(clayton.campus.get_location_by_name('Campus Centre'), 2))

    # Sample test cases
    assert (
        clayton.greedy_student(
            clayton.campus.get_location_by_name("Menzies Building"), 1
        )
        == 22
    ), "Greedy student should collect 22 reward"
    assert (
        clayton.greedy_student(clayton.campus.get_location_by_name("Campus Centre"), 3)
        == 41
    ), "Greedy student should collect 41 reward"
    assert (
        clayton.greedy_student(clayton.campus.get_location_by_name("Campus Centre"), 4)
        == 54
    ), "Greedy student should collect 54 reward"
    print(clayton.total_difficulty(clayton.campus.get_location_by_name("New Horizons")))

    # assert clayton.total_difficulty(clayton.campus.get_start_location()) == 190, "Total difficulty should be 190"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"
    # assert clayton.greedy_student(clayton.campus.get_location_by_name('New Horizons'), 3) == 13, "Greedy student should collect 13 reward"

    # Add test code here
    # print("Clayton")
    # clayton = Exploration("clayton")
    # for campus_location in clayton.campus.get_all_locations():
    #     print(campus_location)
    # print()
    # print(clayton.campus.get_location_by_name('Menzies Building'))
    # print(clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1))
    # print(clayton.greedy_student(clayton.campus.get_location_by_name('New Horizons'), 3))
    # print(clayton.greedy_student(clayton.campus.get_location_by_name('Campus Centre'), 2))
    # print(clayton.total_difficulty(clayton.campus.get_location_by_name('Learning and Teaching Building')))
    # print(clayton.total_reward_for_longest_path(clayton.campus.get_location_by_name('Menzies Building')))
    # menzies = clayton.campus.get_location_by_name('Menzies Building')
    # conn = menzies.get_connections()
    # print(conn.delete_at_index(0))
    # print(clayton.campus.get_location_by_name('Menzies Building'))

    # print(clayton.campus.get_all_locations())
    # print(clayton.campus.get_location_by_name('Campus Centre'))
    # print(clayton.campus.get_location_by_name('Learning and Teaching Building'))

    # print("Malaysia")
    # malaysia = Exploration("malaysia")
    # for campus_location in malaysia.campus.get_all_locations():
    #     print(campus_location)
