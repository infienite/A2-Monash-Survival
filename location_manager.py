from campus import Campus, Location
from data_structures import (
    LinkedList,
    BinarySearchTree,
    ArrayList,
    HashTableSeparateChaining,
)
from data_structures.node_binary import BinaryNode
from algorithms import merge_sort


def calculate_desirability(location: Location) -> float:
    """Calculate desirability of a location."""
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
    """Raise value error if score is invalid type."""
    if type(score) != int and type(score) != float:
        raise ValueError("score argument must be a number")


def validate_k_argument(k: int, num_of_locations: int):
    """Raise value error if k is invalid type."""
    if type(k) != int or not (k > 0 and k <= num_of_locations):
        raise ValueError(
            f"k argument must be a positive integer whose value is between 1 and {num_of_locations}."
        )


class LocationManager:
    def __init__(self, campus_name):
        """
        Best and worst case time complexity is O(C + N log N) where N is the number of locations while C is the number of
        connections of the campus.
        Best and worst case happens when there are N locations and C connections. The function calculates the
        desirability of N locations. Each location have Ci connections where i is the ith node and Ci is the
        number of connections at node i. In total, C1 + C2 + ... + Ci is equal to C. Thus, the operation takes
        O(C+N) time. After that, the function sorts the location list using merge sort. This function takes 
        O(N log N) time to sort all locations inside the list based on the desirability value. Lastly, the
        function creates Binary Search Tree from the sorted location list taking desirability as the key taking
        O(N log N) time in order to insert N elements which takes O(log N) time in each insertion. So, the function
        takes O(C + N log N) time in best and worst case time complexity.
        """
        # Get campus data
        self.campus: Campus = Campus(campus_name)

        # Get locations list
        all_location = self.campus.get_all_locations()

        # Hash table for looking up desirability value based on location name
        self.desirability_lookup = HashTableSeparateChaining(len(all_location))

        # Calculate desirability of each location. Store in lookup (Note: complexity of this for loop is O(N+C) as it visits all N locations and C connections once)
        for location in all_location:

            # Calculate desirability of the location
            desirability = calculate_desirability(location)

            # Add into lookup and sorted list
            self.desirability_lookup.insert(location.get_name(), desirability)

        # Initialize search tree that searches location based on desirability
        self.location_search_tree = BinarySearchTree()

        def create_binary_tree_aux(
            sorted_location: ArrayList[Location], i: int, j: int
        ) -> BinaryNode:
            """Builds a balanced binary tree by taking middle element as the root, then divides the list into left and right partitions and taking the middle elements of each partition as the left and right child respectively until all elements has been added into the tree."""
            # Base case. The left index is more than right index.
            if i > j:
                return None

            # Find middle index
            mid = (i + j) // 2

            # Add desirability and location into the tree
            location = sorted_location[mid]
            self.location_search_tree[self.desirability_lookup[location.get_name()]] = (
                location
            )

            # Builds left and right child
            create_binary_tree_aux(sorted_location, i, mid - 1)
            create_binary_tree_aux(sorted_location, mid + 1, j)

        # Convert from LinkedList to ArrayList for sorting
        all_location_arrlist = ArrayList(len(all_location))
        for location in all_location:
            all_location_arrlist.append(location)

        # Sort locations before building binary search tree
        sorted_locations = merge_sort.merge_sort(
            all_location_arrlist, key=lambda x: self.desirability_lookup[x.get_name()]
        )

        # Build binary search tree based on desirability as the key
        create_binary_tree_aux(sorted_locations, 0, len(sorted_locations) - 1)

    def get_locations_in_range(self, min_score, max_score):
        """
        Best case time complexity is O(1).
        Best case happens when the root of the tree has `root.key > max_score` which halts the
        function early without going through its left and right child.

        Worst case time complexity is O(N) where N is the number of locations inside the tree.
        Worst case happens when all locations inside the tree have `min_score <= desirability <= max_score`.
        The function visits all N locations inside the tree using inorder traversal.
        """
        # Validate arguments
        validate_score_argument(min_score)
        validate_score_argument(max_score)

        # Output list
        locations_in_range = LinkedList()

        for location in self.location_search_tree:

            # Base case. Key is larger than the max score
            if location[0] > max_score:
                break

            # When key is in range, append to output list
            if location[0] >= min_score:
                locations_in_range.append((location[0], location[1].get_name()))

        return locations_in_range

    def get_top_k_locations(self, k):
        """
        Best and worst case time complexity is O(K + log N) where K is the integer representing
        the number of locations to return from the function and N is the number of locations inside
        the tree.
        Best and worst case happens when the root of the tree is traversed to the right most leave
        of the tree. The rightmost leaf contains the location which have the largest desirability value.
        This takes O(log N) time. Then, the function adds the location into an output list and traverse
        to the next location with the largest desirability value. This process repeats for K times until
        all top K locations has been added to the output list. As a result, the function takes O(K + log N)
        time in the best and worst case time complexity.
        """
        # Validate argument
        validate_k_argument(k, len(self.location_search_tree))

        # Output list
        top_k_locations = LinkedList()

        def get_top_k_locations_aux(node: BinaryNode, counter: int) -> int:
            """Fills the output list with top K locations from the tree."""
            # Go to next rightmost child when the node is not empty
            if node:
                # Go to next location and wait for counter value return
                updated_counter = get_top_k_locations_aux(node.right, counter)

                # Add the location into the output list if the counter is still more than 0
                if updated_counter > 0:
                    top_k_locations.append((node.key, node.item.get_name()))
                    updated_counter = get_top_k_locations_aux(node.left, updated_counter-1)

                # Return counter - 1 to signal previous function to either continue or stop adding element into the output list.
                return updated_counter
            # Base case. Return k to signal previous function to start adding element into output list.
            else:
                return counter

        # Build the output list
        get_top_k_locations_aux(self.location_search_tree._root, k)

        # Return the top K locations
        return top_k_locations

    def update_location(self, name, new_reward):
        """
        Best case time complexity is O(1).
        Best case happens when the the new reward of the location is equal to the current reward
        of the location. The function halts early.

        Worst case time complexity is O(log N) where N is the number of locations inside the tree.
        Worst case happens when the new reward is different from the current reward. The function
        calculates a new desirability value using pre-calculated average difficulty value. As a
        result, calculating the new desirability takes O(1) time. Then, the function deletes the
        location with the old desirability value. This takes O(log N) time. This happens because
        about log N nodes are traversed in order to find the location with the desirability value.
        After that, the function adds the new location with new desirability value. This takes
        O(log N) time as about log N nodes are traversed again in order to find the correct insertion
        position. As a result, the function takes O(log N) time to update the location reward.
        """
        # Check whether the name exist inside the tree
        try:
            desirability = self.desirability_lookup[name]
        except KeyError:
            raise ValueError(f"name of location does not exist")

        # Halts early if new reward is equal to previous reward
        reward = self.campus.get_location_by_name(name).get_reward()
        if new_reward == reward:
            return

        # Get the location by name
        location: Location = self.location_search_tree[desirability]

        # Update location reward
        location.set_reward(new_reward)

        # Calculate avg difficulty based on modified formula. Avg diff = reward / desirability - 1 
        avg_diff = reward / desirability - 1
        
        # Calculate the new desirability
        new_desirability = round(new_reward / (1 + avg_diff), 2)

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


if __name__ == "__main__":
    location_manager = LocationManager("clayton")
    print(location_manager.get_locations_in_range(0.87, 1000))
    print(location_manager.get_top_k_locations(5))
    location_manager.update_location("Law Building and Library", 14)
    print(location_manager.get_locations_in_range(0.86, 6))
    print(location_manager.get_top_k_locations(10))


    # Add test code here
