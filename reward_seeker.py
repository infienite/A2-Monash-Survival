from campus import Campus, Location
from data_structures import ArrayR, LinkedList
from reward_structure import UniqueArrayMaxHeap


def get_heap_key(location: Location):
    """Take the location `reward` and `name` as heap key."""
    return (location.get_reward(), location.get_name())


def validate_k_argument(
    k: int,
):
    """Validate `k` argument. `k` must be a positive integer."""
    if type(k) != int or k < 0:
        raise ValueError("k argument must be a positive integer")


class RewardSeeker:
    def __init__(self, campus_name):
        """
        Best and worst case time complexity is O(N) where N is the number of locations.
        Best and worst case happens when N locations are added into the heap. When the heap
        is initialized, the heap is built using bottom-up construction. The copy operation
        takes O(N) time to copy the array elements into a heap array. The sink operation
        on the other hand places takes O(log N) because it traverse through each level of the
        tree to place sink element to the correct position. This operation only occurs to
        log N nodes, and the complexity for sink operation on log N nodes is ignored.
        """
        self.campus: Campus = Campus(campus_name)

        # Get all locations
        all_locations: LinkedList[Location] = self.campus.get_all_locations()

        # Convert locations list from LinkedList to ArrayR
        all_locations_arr: ArrayR = ArrayR(len(all_locations))
        i = 0
        for location in all_locations:
            all_locations_arr[i] = get_heap_key(location)
            i += 1

        # Initialize max heap
        self.reward_max_heap = UniqueArrayMaxHeap.heapify(all_locations_arr)

    def get_next_location(self):
        """
        Best and worst case time complexity is O(log N) where N is the number of elements
        inside the heap.
        Best and worst case happens when there are N elements inside the heap. The maximum
        element is always at the root of the heap and takes O(1). The removal of the element
        causes sink operation to be performed in order to maintain heap invariant of the
        maximum element being at the top of the max heap. Sink operation takes O(log N)
        as the the tree is traversed at log N level.
        """
        # Return None when the heap is empty
        if self.reward_max_heap.is_empty():
            return None
        
        # Get max element inside the heap
        return self.reward_max_heap.extract_root()

    def get_top_k_locations(self, k):
        """
        Best and worst case time complexity is O(k log N) where k is the argument provided and
        N is the number of elements inside the heap.
        Best and worst case happens when there are N elements inside the heap and k <= N. The
        max element is removed from the heap taking log N time for k times in total. When
        k > N, the function will halts after N time and takes O(k log N) where k = N.
        """
        # Validate argument
        validate_k_argument(k)

        # Output list
        top_k_locations = LinkedList()

        # Call get max for k time if k < N. Else call for N time.
        for _ in range(k):

            # Stop adding location if the heap is empty
            if self.reward_max_heap.is_empty():
                break

            # Add location if the heap is not empty
            top_k_locations.append(self.reward_max_heap.extract_root())

        # Return output list
        return top_k_locations

    def update_location_reward(self, location_name, new_reward):
        """
        Best case time complexity is O(1).
        Best case happens when the new location reward is equal to the current location reward.
        The update function of the heap halts early because no changes occurred to the node and
        thus no update need to be done to the structure of the heap.

        Worst case time complexity is O(log N) where N is the number of elements inside the heap.
        Worst case happens when there are N elements inside the heap and the new reward is more
        than or less than the current reward. When the new reward is larger, the rise operation
        swaps the heap element with its parent for up to log N times until it reaches the correct
        position. When the new reward is smaller, the sink operation swaps the heap element with
        its child up to log N times or the depth of the tree until reaches the correct position.
        """
        # Get location by name
        location = self.campus.get_location_by_name(location_name)
        current_key = get_heap_key(location)

        # Update location reward
        location.set_reward(new_reward)

        # Get new key of
        new_key = get_heap_key(location)

        # Update the new reward inside the max heap
        self.reward_max_heap.update(current_key, new_key)


if __name__ == "__main__":
    reward_seeker = RewardSeeker("clayton")

    # print(reward_seeker.get_next_location())
    # # reward_seeker.update_location_reward('Monash Club', 1000)
    # print(reward_seeker.get_top_k_locations(3))
    # reward_seeker.update_location_reward("Campus Centre", 100)
    # print(reward_seeker.get_top_k_locations(2))

    # Add test code here
