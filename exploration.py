from campus import Campus, Location, Connection
from data_structures import LinkedList

class Exploration:
    def __init__(self, campus_name):
        self.campus = Campus(campus_name)

    def greedy_student(self, location: Location, stamina: int):
        """
        Analyse your time complexity of this method.
        """
        conns = location.get_connections()
        if stamina == 0 or len(conns) == 0:
            return location.get_reward()
        
        temp: Connection = conns.delete_at_index(0)
        next_conn: Connection = temp

        for conn in conns:
            if conn.get_difficulty() == next_conn.get_difficulty() \
                and conn.get_location().get_reward() > next_conn.get_location().get_reward() \
                or conn.get_difficulty() < next_conn.get_difficulty():
                next_conn = conn

        conns.insert(0, temp)

        return location.get_reward() + self.greedy_student(next_conn.get_location(), stamina-1)

    def total_difficulty(self, location: Location):
        """
        Time complexity analysis not required for this method.
        """

        def total_difficulty_aux(location: Location, prev_total_diff: int):
            
            conns = location.get_connections()

            if len(conns) == 0:
                return prev_total_diff

            total_diff = 0
            for conn in conns:
                conn: Connection = conn
                total_diff += total_difficulty_aux(conn.get_location(), prev_total_diff + conn.get_difficulty())

            return total_diff

        return total_difficulty_aux(location, 0)


    def total_reward_for_longest_path(self, location: Location):
        """
        Time complexity analysis not required for this method.
        """
        def total_reward_for_longest_path_aux(location: Location, length: int, total_reward: int=0):
            
            conns = location.get_connections()

            if len(conns) == 0:
                return (length, total_reward + location.get_reward())
            
            temp: Connection = conns.delete_at_index(0)
            ml, mr = total_reward_for_longest_path_aux(temp.get_location(), length+1, total_reward + location.get_reward())
            
            for conn in conns:
                conn: Connection = conn
                l, r = total_reward_for_longest_path_aux(conn.get_location(), length+1, total_reward + location.get_reward())
                if l == ml and r > mr or l > ml:
                    ml = l
                    mr = r
            
            conns.insert(0, temp)

            return (ml, mr)

        return total_reward_for_longest_path_aux(location, 1)[1]

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    # print("Clayton")
    # clayton = Exploration("clayton")
    # for campus_location in clayton.campus.get_all_locations():
    #     print(campus_location)
    # print()
    clayton = Exploration('clayton')
    # print(clayton.campus.get_location_by_name('Menzies Building'))
    print(clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1))
    print(clayton.greedy_student(clayton.campus.get_location_by_name('Campus Centre'), 2))
    print(clayton.total_difficulty(clayton.campus.get_location_by_name('Learning and Teaching Building')))
    print(clayton.total_reward_for_longest_path(clayton.campus.get_location_by_name('Menzies Building')))
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

    # Sample test cases
    assert clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1) == 22, "Greedy student should collect 22 reward"
    assert clayton.total_difficulty(clayton.campus.get_start_location()) == 190, "Total difficulty should be 190"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"

    # Add test code here
