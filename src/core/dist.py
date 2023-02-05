from collections import defaultdict

class Dist(dict):

    def __init__(self, data=None):
        dist = self.create_distribution(data if data else [])
        self.total = len(dist)
        super().__init__(dist)

    @staticmethod
    def create_distribution(data) -> dict:
        dist = defaultdict(int)
        n = len(data)
        for o in data:
            dist[o] += 1
        return {key:val/n for key,val in dist.items()}

