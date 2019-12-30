from jyutping_dict import JyutpingDict
import numpy as np

class SentenceGraph:
    """
    TODO: Go back and optimize with numpy
    """ 
    def __init__(self, jd, distr):
        """
        Initializes SentenceGraph with a Jyutping dictionary
        and trigram distribution.

        Args:
            jd: The JyutpingDict object that provides the mapping
                from Jyutping to valid possible characters

            distr: Distribution object representing the n-gram distribution 
        """ 
        self.jd = jd
        self.distr = distr

    def generate(self, jyutping_list):
        """
        Generates the Trelli graph that represents the Markov transitions.
        First part of the Viterbi Algorithm

        Args:
            jyutping_list:
                List of consecutive Jyutping syllables
                Ex: ["pin", "yin", "shu", "ru", "fa"]
        Variables:
            state_space: List of lists of all possible states at each index
                eg. [['拼','品', ...,],['书', '输', '熟', ...],['发', ...],...] 
            init_probs: Probabilities of the initial possible states
            state_map: List providing map from index to character
            reverse_map: Dict mapping from character to index in state_map
            emission[i][j]: Pr(obs j | state i), values are 0 or 1
            transition[s_i][s_j]: Pr(s_i | s_j) where s_i and s_j are
                the indicies that correspond to the two characters in
                state_map
        """ 
        jyut_l = self.jyutping_list
        self.state_space = list(map(self.jd.match, jyut_l))
        self.init_probs = np.array(map(self.distr.prob, state_space[0]))
        self.state_map = list({s for s in l for l in self.state_space})
        self.reverse_map = {s : idx for idx,s in enumerate(self.state_map)}

        N,M = len(jl), len(self.state_map)
        self.emission = np.zeros((N,M))
        for i in range(M):
            for j in range(N):
                ch = self.state_map[i]
                if ch in self.jd.jyut2char(jyut_l[j]):
                    self.emission[j][i] = 1
        
        self.transition = np.ndarray((M,M))
        for i in range(M):
            for j in range(M):
                s_i, s_j = self.state_map(i), self.state_map(j)
                self.transition[i][j] = self.distr.posterior(s_i, s_j) 
        
    def viterbi(self):
        """
        Returns the word sequence to the MAP of the HMM,
        equivalent to finding the optimal path on trelli graph.
        
        Heavily and shamelessly inspired by (thanks in advance):
            https://stackoverflow.com/questions/9729968/python-implementation-of-viterbi-algorithm
            user: RBF06

        Parametetrs:
            y : array (M,)
                Observation state sequence. int dtype.
            A : array (K, K)
                State transition matrix. See HiddenMarkovModel.state_transition  for
                details.
            B : array (K, M)
                Emission matrix. See HiddenMarkovModel.emission for details.
            Pi: optional, (K,)
                Initial state probabilities: Pi[i] is the probability x[0] == i. If
                None, uniform initial distribution is assumed (Pi[:] == 1/K).

            Returns
            -------
            x : array (T,)
                Maximum a posteriori probability estimate of hidden state trajectory,
                conditioned on observation sequence y under the model parameters A, B,
                Pi.
            T1: array (K, T)
                the probability of the most likely path so far
            T2: array (K, T)
                the x_j-1 of the most likely path so far
        """
        A = self.transition
        B = self.emission
        # Cardinality of the state space
        K = A.shape[0]
        # Initialize the priors with default (uniform dist) if not given by caller
        Pi = self.init_probs
        T = len(self.jyutping_list)
        T1 = np.empty((K, T), 'd')
        T2 = np.empty((K, T), 'B')

        # Initilaize the tracking tables from first observation
        T1[:, 0] = Pi * B[:, 0]
        T2[:, 0] = 0

        # Iterate throught the observations updating the tracking tables
        for i in range(1, T):
            T1[:, i] = np.max(T1[:, i - 1] * A.T * B[np.newaxis, :, i].T, 1)
            T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)

        # Build the output, optimal model trajectory
        x = np.empty(T, 'B')
        x[-1] = np.argmax(T1[:, T - 1])
        for i in reversed(range(1, T)):
            x[i - 1] = T2[x[i], i]

        return x, T1, T2