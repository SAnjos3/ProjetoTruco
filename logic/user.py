import hashlib

class User:
    def __init__(self, username, password, name):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.name = name
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class Player(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name)
        self.score = 0
    
    def update_score(self, points):
        self.score += points
