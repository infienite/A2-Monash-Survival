from campus import Campus, Location
from data_structures import LinkedList, BinarySearchTree, ArrayList, HashTableSeparateChaining
from data_structures.node_binary import BinaryNode
from algorithms import merge_sort


def calculate_desirability(location: Location) -> float:
    """ Calculate desirability of a location. """
    # Get all connections of the location
    conns = location.get_connections()

    # Calculate total difficulty of the location
    total_diff = 0
    for conn in conns:
        total_diff += conn.get_difficulty()
    
    # Calculate average difficulty. If no connection, average difficulty set to 0.
    avg_diff = 0 if len(conns) == 0 else total_diff / len(conns)
    
    # Calculate desirability = reward / (1 + average difficulty)
    reward = location.get_reward()
    return round(reward / (1 + avg_diff), 2)


def validate_score_argument(score: int | float):
    """ Raise value error if score is invalid type. """
    if type(score) != int and type(score) != float:
        raise ValueError('score argument must be a number')
    

def validate_k_argument(k: int, num_of_locations: int):
    """ Raise value error if k is invalid type . """
    if type(k) != int or not(k > 0 and k <= num_of_locations):
        raise ValueError('k argument must be a positive integer whose value is between 1 and number of locations (inclusive).')


class LocationManager:
    def __init__(self, campus_name):
        """
        Best and worst case time complexity is O(C + N log N) where N is the number of locations while C is the number of
        connections of the campus.
        Best and worst case happens when there are N interconnected locations with C connections. The function will
        calculate the desirability of each location which requires iterating through all N locations and in each
        of the iteration, the function will loop through all connection's difficulty level Ci times in total where
        i represent node i and Ci represent the number of connection of node i. After that, the function will run
        mergesort on location list, costing O(N log N) before creating the Binary Search Tree. The function finally
        creates the Binary Search Tree, costing O(N log N) to create each location representation inside the tree
        and arranging them at the correct position inside the tree.
        """
        # Get campus data
        self.campus: Campus = Campus(campus_name)
        
        # Get locations list
        all_location = self.campus.get_all_locations()

        # Hash table for looking up desirability value based on location name
        self.desirability_lookup = HashTableSeparateChaining(len(all_location))

        # Calculate desirability of each location. Store in lookup
        for location in all_location:

            # Calculate desirability of the location
            desirability = calculate_desirability(location)

            # Add into lookup and sorted list
            self.desirability_lookup.insert(location.get_name(), desirability)

        # Initialize search tree that searches location based on desirability 
        self.location_search_tree = BinarySearchTree()

        def create_binary_tree_aux(sorted_location: ArrayList[Location], i: int, j: int) -> BinaryNode:
            """ Builds binary tree by taking middle element as the root, then divides the list into left and right partitions as left and right child respectively. """
            # Base case. The left index is more than right index.
            if i > j:
                return None
            
            # Find middle index
            mid = (i + j) // 2

            # Add desirability and location into the tree
            location = sorted_location[mid]
            self.location_search_tree[self.desirability_lookup[location.get_name()]] = location

            # Builds left and right child
            create_binary_tree_aux(sorted_location, i, mid-1)
            create_binary_tree_aux(sorted_location, mid+1, j)

        # Convert from LinkedList to ArrayList for sorting
        all_location_arrlist = ArrayList(len(all_location))
        for location in all_location:
            all_location_arrlist.append(location)

        # Sort locations before building binary search tree
        sorted_locations = merge_sort.merge_sort(all_location_arrlist, key=lambda x: self.desirability_lookup[x.get_name()])

        # Build binary search tree based on desirability as the key
        create_binary_tree_aux(sorted_locations, 0, len(sorted_locations)-1)

    def get_locations_in_range(self, min_score, max_score):
        """
        Best case time complexity is O(1).
        Best case happens when the root of the tree has `root.key > max_score` which halts the
        function early without going through its left and right child and so on. The function
        run only once.

        Worst case time complexity is O(N) where N is the number of nodes inside the tree.
        Worst case happens when all nodes inside the tree have `min_score < node.key < max_score`.
        The function will visit all nodes inside the tree in inorder traversal pattern for
        N times.
        """
        # Validate arguments
        validate_score_argument(min_score)
        validate_score_argument(max_score)

        # Output list
        locations_in_range = LinkedList()

        def get_locations_in_range_aux(node: BinaryNode) -> None:
            # Checks whether node's key value is in between score range
            if node:

                # Inorder traversal by visiting all left child first
                get_locations_in_range_aux(node.left)
                
                # Base case. Key is larger than the max score
                if node.key > max_score:
                    return
                
                # When key is in range, append to output list
                if node.key >= min_score:
                    locations_in_range.append((node.key, node.item.get_name()))
                
                # Visit the right child only after visiting the left child and the parent
                get_locations_in_range_aux(node.right)

        # The accumulator function perform computation and updates the output list
        get_locations_in_range_aux(self.location_search_tree._root)
        return locations_in_range

    def get_top_k_locations(self, k):
        """
        Best and worst case time complexity is O(K + log N) where K is the integer representing
        the number of locations to return from the function and N is the number of locations inside
        the tree. 
        Best and worst case happens when the search happens from the root of the tree to the rightmost
        leaf from the root which takes O(log N) time. Since the rightmost leaf contains the largest
        desirability value, the function adds the leaf node to the output list. Then, the function
        returns the counter for the previous function call to signal that k-1 location has been added
        to the output list. This process happens for K time in total. After the final top location
        has been added, the function will stop adding location to the output list.
        """
        # Validate argument
        validate_k_argument(k, len(self.location_search_tree))

        # Output list
        top_k_locations = LinkedList()

        def get_top_k_locations_aux(node: BinaryNode) -> int:
            """ Fills the output list with top K locations from the tree. """
            # Go to next rightmost child when the node is not empty
            if node:
                # Go to next location and wait for counter value return
                counter = get_top_k_locations_aux(node.right)

                # Add the location into the output list if the counter is still more than 0
                if counter > 0:
                    top_k_locations.append((node.key, node.item.get_name()))

                # Return counter - 1 to signal previous function to either continue or stop adding element into the output list. 
                return counter-1
            # Base case. Return k to signal previous function to start adding element into output list.
            else:
                return k
            
        # Build the output list
        get_top_k_locations_aux(self.location_search_tree._root)

        # Return the top K locations
        return top_k_locations

    def update_location(self, name, new_reward):
        """
        Best case time complexity is O(1).
        Best case happens when the the new reward of the location is equal to the current reward
        of the location. The function halts early and the tree is not updated.

        Worst case time complexity is O(log N) where N is the number of locations inside the tree.
        Worst case happens when the new reward cause the tree to be updated. Updating the tree
        requires deleting the location with the old desirability value and inserting the location
        with the new desirability value. It takes O(log N) to delete the node and add them back
        into the tree as a traversal need to be done for both tree operations.
        """
        # Check whether the name exist inside the tree
        try:
            desirability = self.desirability_lookup[name]
        except KeyError:
            raise ValueError(f'name of location does not exist')
        
        # Halts early if new reward is equal to previous reward
        reward = self.campus.get_location_by_name(name).get_reward()
        if new_reward == reward:
            return
        
        # Get the location by name
        location: Location = self.location_search_tree[desirability]
        
        # Update location reward
        location.set_reward(new_reward)

        # Calculate new desirability
        new_desirability = calculate_desirability(location)

        # Delete the old location by old desirability
        del self.location_search_tree[desirability]

        # Add location with new desirability in the tree
        self.location_search_tree[new_desirability] = location

        # Update lookup table with new desirability
        self.desirability_lookup[name] = new_desirability
        
    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    location_manager = LocationManager('clayton')
    print()
    print(location_manager.get_locations_in_range(1.5, 6))
    print()
    print(location_manager.get_top_k_locations(4))
    location_manager.update_location('Law Building and Library', 14)
    print(location_manager.get_locations_in_range(1.5, 6))

    # Add test code here
