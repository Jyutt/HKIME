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
        self.single_counter = {}
        self.ngram_count = 0
        self.singles_count = 0

    def add_occurence(self, n_gram, count=1):
        assert len(n_gram) == 3

        if n_gram[:2] not in self.counter:
            self.counter[n_gram[:2]] = {}
        if n_gram[2] not in self.counter[n_gram[:2]]:
            self.counter[n_gram[:2]] = count
            self.ngram_count += 1
        else:
            self.counter[n_gram[:2]] += count

        for w in n_gram:
            if w not in self.single_counter:
                self.single_counter[w] = count
            else:
                self.single_counter[w] += count
        self.singles_count += count * 3

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


class BiGramDistribution(Distribution):
    """
    FOR QUICK PROTOTYPING / TESTING purposes only
    We will be using trigrams for the language model.
    BiGramDistribution is only for testing out the Viterbi
    algorithm implementation in graph.py before generalizing
    to trigrams
    """

    def add_occurence(self, bi_gram, count=1):
        assert len(bi_gram) == 2

        if bi_gram[0] not in self.counter:
            self.counter[bi_gram[0]] = {}
        if bi_gram[1] not in self.counter[bi_gram[0]]:
            self.counter[bi_gram[0]][bi_gram[1]] = count
            self.ngram_count += 1
        else:
            self.counter[bi_gram[0]][bi_gram[1]] += count

        for w in bi_gram:
            if w not in self.single_counter:
                self.single_counter[w] = count
            else:
                self.single_counter[w] += count
        self.singles_count += count * 2
