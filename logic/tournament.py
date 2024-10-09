class Tournament:
    def __init__(self, name):
        self.name = name
        self.matches = []
    
    def add_match(self, match):
        self.matches.append(match)
    
    def get_total_scores(self):
        total_scores = {}
        for match in self.matches:
            for username, score in match.scores.items():
                total_scores[username] = total_scores.get(username, 0) + score
        return total_scores