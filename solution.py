class Solution:
    def __init__(self, queue):
        self.queue = queue
        self.score = float('-inf')

    def __repr__(self):
        return f"{self.queue}\nScore: {self.score}"

    def set_score(self, score):
        self.score = score