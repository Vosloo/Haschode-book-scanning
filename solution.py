class Solution:
    def __init__(self, genotype):
        self.genotype = genotype
        self.score = float("-inf")

    def __len__(self):
        return len(self.genotype)

    def __getitem__(self, key):
        return self.genotype[key]

    def __setitem__(self, key, value):
        self.genotype[key] = value

    def set_score(self, score):
        self.score = score