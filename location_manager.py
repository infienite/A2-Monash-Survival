from campus import Campus, Location, Connection
from data_structures import ArraySortedList, LinkedList, BinarySearchTree, LinkedQueue, LinkedStack, ArrayList, HashTableSeparateChaining
from data_structures.node_binary import BinaryNode

class LocationManager:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """

        self.campus: Campus = Campus(campus_name)
        
        all_location = self.campus.get_all_locations()

        location_desireability_sorted = ArraySortedList(len(all_location))
        self.lookup = HashTableSeparateChaining(len(all_location))

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
            location_desireability_sorted.add((desirability, location.get_name()))
            self.lookup.insert(location.get_name(), desirability)

        self.tree_root = BinarySearchTree()

        def create_binary_tree_aux(location_desireability_sorted: tuple, i: int, j: int) -> BinaryNode:
            if i > j:
                return
            mid = (i+j)//2
            location = location_desireability_sorted[mid]
            self.tree_root[(-location[0], location[1])] = location[0]
            create_binary_tree_aux(location_desireability_sorted, i, mid-1)
            create_binary_tree_aux(location_desireability_sorted, mid+1, j)

        create_binary_tree_aux(location_desireability_sorted, 0, len(location_desireability_sorted)-1)

    def get_locations_in_range(self, min_score, max_score):
        """
        Analyse your time complexity of this method.
        """
        ranged_location_desireability = LinkedList()
        for node in self.tree_root:
            if node[1] >= min_score and node[1] <= max_score:
                ranged_location_desireability.insert(0, (node[1], node[0][1]))
        return ranged_location_desireability

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """        
        top_k_location_desireability = LinkedList()

        if k == 0:
            return top_k_location_desireability

        for node in self.tree_root:
            if len(top_k_location_desireability) == k:
                if node[1] <= top_k_location_desireability[0][0]:
                    break
                top_k_location_desireability.delete_at_index(len(top_k_location_desireability)-1)
                top_k_location_desireability.append((node[1], node[0][1]))
            else:
                top_k_location_desireability.append((node[1], node[0][1]))
 
        return top_k_location_desireability

    def update_location(self, name, new_reward):
        """
        Analyse your time complexity of this method.
        """
        for n in self.tree_root:
            print(n)
        desireability = self.lookup[name]
        key = (-desireability, name)
        del self.tree_root[key]
        loc: Location = self.campus.get_location_by_name(name)
        avg_diff = loc.get_reward() / desireability - 1
        print(avg_diff)
        loc.set_reward(new_reward)
        desirability = round(new_reward / (1 + avg_diff), 2)
        nkey = (-desirability, name)
        self.tree_root[nkey] = desirability
        for n in self.tree_root:
            print(n)
        
    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    location_manager = LocationManager('clayton')
    print()
    print(location_manager.get_locations_in_range(2.4, 6))
    print()
    print(location_manager.get_top_k_locations(4))
    print(location_manager.update_location('New Horizons', 1000))
    # Add test code here
