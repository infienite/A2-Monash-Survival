from campus import Campus, Location
from data_structures import HashTableSeparateChaining, ArrayList, ArrayR, LinkedList
from reward_structure import ArrayMaxHeap

class RewardSeeker:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        self.campus: Campus = Campus(campus_name)
        locs: LinkedList[Location] = self.campus.get_all_locations()
        arr: ArrayR = ArrayR(len(locs))
        self.lookup = HashTableSeparateChaining(len(locs))
        
        i = 0
        for loc in locs:
            arr[i] = (loc.get_reward(), loc.get_name())
            self.lookup[loc.get_name()] = loc.get_reward()
            i += 1

        # print(arr)
        self.heap = ArrayMaxHeap(len(locs), arr)

    def get_next_location(self):
        """
        Analyse your time complexity of this method.
        """
        return self.heap.get_max()

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """
        o = LinkedList()
        for _ in range(k):
            o.append(self.heap.get_max())
        return o

    def update_location_reward(self, location_name, new_reward):
        """
        Analyse your time complexity of this method.
        """
        r = self.lookup[location_name]
        self.heap.update((r, location_name), (new_reward, location_name))
        loc: Location = self.campus.get_location_by_name(location_name)
        loc.set_reward(new_reward)

if __name__ == '__main__':
    reward_seeker = RewardSeeker('clayton')

    # print(reward_seeker.get_top_k_locations(3))
    reward_seeker.update_location_reward('Monash Club', 1000)
    print(reward_seeker.get_top_k_locations(3))
    reward_seeker.update_location_reward('Campus Centre', 67)
    print(reward_seeker.get_next_location())

    # Add test code here
