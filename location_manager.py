from campus import Campus, Location, Connection
from data_structures import ArraySortedList, LinkedList, BinarySearchTree, LinkedQueue, LinkedStack
from data_structures.node_binary import BinaryNode

class LocationManager:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
            
        
        self.campus: Campus = Campus(campus_name)
        
        all_location = self.campus.get_all_locations()

        location_desireability_sorted = ArraySortedList(len(all_location))

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

        def create_binary_tree_aux(location_desireability_sorted: tuple, i: int, j: int) -> BinaryNode:
            if i > j:
                return None
            mid = (i+j)//2
            location = location_desireability_sorted[mid]
            node = BinaryNode(location)
            node.left = create_binary_tree_aux(location_desireability_sorted, i, mid-1)
            node.right = create_binary_tree_aux(location_desireability_sorted, mid+1, j)
            return node

        self.location_desireability_tree = create_binary_tree_aux(location_desireability_sorted, 0, len(location_desireability_sorted)-1)

    def get_locations_in_range(self, min_score, max_score):
        """
        Analyse your time complexity of this method.
        """
        ranged_location_desireability = LinkedList()
        def get_locations_in_range_aux(node: BinaryNode) -> None:
            if node:
                get_locations_in_range_aux(node.left)
                
                if node.item[0] >= min_score and node.item[0] <= max_score:
                    ranged_location_desireability.append(node.item)
                
                get_locations_in_range_aux(node.right)
        get_locations_in_range_aux(self.location_desireability_tree)
        return ranged_location_desireability

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """
        top_k_location_desireability = LinkedList()
        def get_top_k_locations_aux(node: BinaryNode):
            if node:
                counter = get_top_k_locations_aux(node.right)
                if counter > 0:
                    top_k_location_desireability.append(node.item)
                return counter-1
            else:
                return k
        get_top_k_locations_aux(self.location_desireability_tree)
        return top_k_location_desireability

    def update_location(self, name, new_reward):
        """
        Analyse your time complexity of this method.
        """
        pass

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    location_manager = LocationManager('clayton')
    print(location_manager.location_desireability_tree)
    print()
    print(location_manager.get_locations_in_range(2.4, 6))
    print()
    print(location_manager.get_top_k_locations(3))
    # Add test code here
