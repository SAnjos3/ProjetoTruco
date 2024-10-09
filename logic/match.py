class Match:
    def __init__(self, match_id, players):
        self.match_id = match_id
        self.players = players
        self.scores = {player.username: 0 for player in players}
    
    def update_score(self, player_username, points):
        if player_username in self.scores:
            self.scores[player_username] += points

