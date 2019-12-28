from jyutping_dict import JyutpingDict

class SentenceGraph:
    def __init__(self, jd, distr):
        """
        Initializes SentenceGraph with a Jyutping dictionary
        and trigram distribution.
        TODO: Accept n-gram distributions for any n

        Args:
            jd: The JyutpingDict object that provides the mapping
                from Jyutping to valid possible characters

            distr: Dictionary representing trigram distribution
                   (maybe we need to create a distribution class?
        """
        self._jyutping_dict = jyutping_dict
        self._distr = distr
        self.graph = []
        self.jyutping_list = []

    def generate(self, jyutping_list):
        """
        Generates the graph based on the list of Jyutping

        Args:
            jyutping_list: List of individual Jyutping syllables corresponding to
                           individual characters
        """

    def solve(self):
        """
        Finds the optimal path in the graph, which is equivalent to
        predicting the most likely sentence / phrase given the Jyutping list

        Use Viterbi?
        """
