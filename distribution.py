import random


class Distribution():
    """
    This class is used to store and represent the probability
    distribution of n-grams. By default, we work with
    trigrams, that is n = 3.
    """
    def __init__(self, n=3):
        self.counter = {}
        self.single_counter = {}
        self.ngram_count = 0
        self.singles_count = 0
        self.n = n

    def add_occurence(self, n_gram, count=1):
        n = self.n
        assert len(n_gram) == n

        if n_gram[:-1] not in self.counter:
            self.counter[n_gram[:-1]] = {}
        if n_gram[-1] not in self.counter[n_gram[:-1]]:
            self.counter[n_gram[:-1]][n_gram[-1]] = count
            self.ngram_count += 1
        else:
            self.counter[n_gram[:-1]][n_gram[-1]] += count

        for w in n_gram:
            if w not in self.single_counter:
                self.single_counter[w] = count
            else:
                self.single_counter[w] += count
        self.singles_count += count * n

    def posterior(self, w, prior):
        """
        return:
            P(w | prior)
        """
        assert len(w) == 1 and len(prior) == 2

        if prior in self.counter:
            total = sum(self.counter[prior].values())
            count = self.counter[prior].get(w)
            return count / total if count else 0  # Check if count is None
        else:
            return 0

    def prob(self, w):
        """
        return:
            P(w)
        """
        if w in self.single_counter:
            return self.single_counter[w] / self.singles_count
        else:
            return 0

    def randomized(self):
        """
        Returns a generator that yields, in a random order, the
        counts and frequnecies of trigrams. This can then be used
        to calculate posterior probability. For SGD training purposes.
        """
        priors = list(self.counter.keys())
        random.shuffle(priors)
        for p in priors:
            total = sum(self.counter[p].values())
            yield p, total, self.counter[p]
