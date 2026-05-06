from campus import Campus

class LocationManager:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        """
        self.campus: Campus = Campus(campus_name)

    def get_locations_in_range(self, min_score, max_score):
        """
        Analyse your time complexity of this method.
        """
        pass

    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.
        """
        pass

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

    # Add test code here
