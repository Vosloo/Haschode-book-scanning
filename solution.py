from typing import List


class Solution:
    def __init__(self, queue):
        self.queue: List = queue
        self.score: float = float('-inf')

    def __repr__(self):
        return f"{self.queue} Score: {self.score}"

    def __len__(self):
        return len(self.queue)

    def set_score(self, score):
        self.score = score