import random


class Distribution():
    """
    This class is used to represent the probability distribution of n-grams
    from an input corpus.  The probability is calculated from
    self.ngram_count, a dictionary that keeps count of n-gram frequencies.
    The probability distribution is then dynamically calculated from the
    frequencies and total number of occurences. This allows for
    dynamic changes to the distribution after initialization.
    We use n=3, i.e tri-grams.
    """
    def __init__(self):
        self.counter = {}
        self.ngram_count = 0

    def add_occurence(self, n_gram, count=1):
        assert len(n_gram) == 3

        if n_gram[:2] not in self.counter:
            self.counter[n_gram[:2]] = {}
        if n_gram[2] not in self.counter[n_gram[:2]]:
            self.counter[n_gram[:2]] = count
            self.ngram_count += 1
        else:
            self.counter[n_gram[:2]] += count

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
