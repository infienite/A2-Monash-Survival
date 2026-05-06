from campus import Campus

class RewardSeeker:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        self.campus: Campus = Campus(campus_name)

    def get_next_location(self):
        """
        Analyse your time complexity of this method.
        """
        pass

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """
        pass

    def update_location_reward(self, location_name, new_reward):
        """
        Analyse your time complexity of this method.
        """
        pass

if __name__ == '__main__':
    reward_seeker = RewardSeeker('clayton')
    # Add test code here
