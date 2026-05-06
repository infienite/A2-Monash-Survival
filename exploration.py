from campus import Campus, Location, Connection
from data_structures import LinkedList

class Exploration:
    def __init__(self, campus_name):
        self.campus = Campus(campus_name)

    def greedy_student(self, location, stamina):
        """
        Analyse your time complexity of this method.
        """
        total_reward = 0
        
        cur_location: Location = location

        while cur_location and stamina >= 0:
        
            connections = cur_location.get_connections()
        
            total_reward += cur_location.get_reward()
            
            temp: Connection = connections.delete_at_index(0)
        
            next_connection: Connection = temp
            
            for connection in connections:
                
                if connection.get_difficulty() == next_connection.get_difficulty() \
                    and connection.get_location().get_reward() > next_connection.get_location().get_reward() \
                    or connection.get_difficulty() < next_connection.get_difficulty():
                    next_connection = connection


            connections.insert(0, temp)
            cur_location = next_connection.get_location()
            stamina -= 1

        return total_reward

    def total_difficulty(self, location):
        """
        Time complexity analysis not required for this method.
        """
        pass

    def total_reward_for_longest_path(self, location):
        """
        Time complexity analysis not required for this method.
        """
        pass

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
    # assert clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1) == 22, "Greedy student should collect 22 reward"
    # assert clayton.total_difficulty(clayton.campus.get_start_location()) == 190, "Total difficulty should be 190"
    # assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"

    # Add test code here
