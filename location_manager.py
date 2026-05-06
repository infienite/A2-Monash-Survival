from campus import Campus, Location, Connection
from data_structures import ArraySortedList, LinkedList

class LocationManager:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        self.campus: Campus = Campus(campus_name)
        
        all_location = self.campus.get_all_locations()

        self.location_desireability = ArraySortedList(len(all_location))

        for location in all_location:
            location: Location = location
            total_diff = 0
            conns = location.get_connections()
            for conn in conns:
                conn: Connection = conn
                total_diff += conn.get_difficulty()
            avg_diff = 0 if len(conns) == 0 else total_diff / len(conns)
            reward = location.get_reward()
            desirability = round(reward / (1 + avg_diff), 2)
            self.location_desireability.add((desirability, location.get_name()))

    def get_locations_in_range(self, min_score, max_score):
        """
        Analyse your time complexity of this method.
        """
        ranged_location_desireability = LinkedList()
        n = len(self.location_desireability)
        i = 0
        while i < n and self.location_desireability[i][0] < min_score:
            i += 1
        
        while i < n and self.location_desireability[i][0] <= max_score:
            ranged_location_desireability.append(self.location_desireability[i])
            i += 1

        return ranged_location_desireability

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """
        top_location_desireability = LinkedList()
        n = len(self.location_desireability)
        for j in range(k):
            top_location_desireability.append(self.location_desireability[n-1-j])
        return top_location_desireability

    def update_location(self, name, new_reward):
        """
        Analyse your time complexity of this method.
        """
        

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    location_manager = LocationManager('clayton')
    print(location_manager.location_desireability)
    print()
    print(location_manager.get_locations_in_range(.86, 2.4))
    print(location_manager.get_top_k_locations(3))
    # Add test code here
