from jyutping_dict import JyutpingDict
from functools import reduce
import numpy as np


class SentenceGraph:
    """
    TODO: Convert examples from pinyin to jyutping.
    Potentially make viterbi algorithm more efficient
    since impossible state transitions are included.
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
                Ex: ["jyut", "ping", "syu", "jap", "faat"]
        self Variables:
            init_probs:
                Probabilities of the initial possible states

            state_map:
                List providing map from index to character
                Ex: 
                    2-grams case: state_map[2] = "粤"
                    3-grams case: state_map[3] = "粵拼"

            reverse_map:
                Dict mapping from character to index in state_map
                Ex: 
                    2-grams case: reverse_map["粤"] = 2
                    3-grams case: reverse_map["粵拼"] = 3

            emission[i][j]:
                Pr(obs j | state i), takes on values of 0 or 1
                Ex:
                    2-grams case: Pr("jyut", "粤") = 1, Pr("ping", "粤") = 0
                    3-grams case: Pr("jyut ping" | "粤拼“) = 1, Pr("ping syu", "粤语") = 0

            transition[s_i][s_j]:
                Transition probability Pr(c_i | c_j) where c_k denotes state_map[k]
                Ex:
                   2-grams case:
                       transition[8][2] = Pr(state_map[8] | state_map[2]) = Pr("拼" | "粵") = 0.33
                   3-grams case:
                       transition[9][3] = Pr(state_map[9] | state_map[3])
                           = Pr("輸入" | "粵拼") = 0
                       tranisition[10][3] = Pr(state_map[10] | state_map[3])
                          = Pr("拼輸" | "粵拼") = 0.10
        TODO: Generalize for arbitrary n for n-grams
              Lint lint lint lint
        """
        self.jyutping_list = jyutping_list
        jyut_l = jyutping_list
        states = list(set(reduce(lambda x, y: x + y, map(self.jd.jyut2char, jyutping_list))))

        if self.distr.n == 2:
            self.state_map = states
            self.reverse_map = {s: idx for idx, s in enumerate(self.state_map)}
            self.init_probs = np.array(list(map(self.distr.prob, self.state_map)))

            N, M = len(jyut_l), len(self.state_map)
            self.emission = np.zeros((N, M))
            for i in range(M):
                for j in range(N):
                    ch = self.state_map[i]
                    if ch in self.jd.jyut2char(jyut_l[j]):
                        self.emission[j][i] = 1

            self.transition = np.ndarray((M, M), dtype="float")
            for i in range(M):
                for j in range(M):
                    s_i, s_j = self.state_map[i], self.state_map[j]
                    self.transition[i][j] = self.distr.posterior(s_i, s_j)
        elif self.distr.n == 3:
            self.state_map = [a + b for a in states for b in states]
            self.reverse_map = {s: idx for idx, s in enumerate(self.state_map)}
            self.init_probs = np.array(list(map(self.distr.prob, self.state_map)))

            N, M = len(jyut_l) - 1, len(self.state_map)
            self.emission = np.zeros((N, M))

            prev_match = self.state_map[0][0] in self.jd.jyut2char(jyut_l[0])
            for i in range(M):
                for j in range(N):
                    cur_match = self.state_map[i][1] in self.jd.jyut2char(jyut_l[i + 1]) # 2nd char
                    if prev_match and cur_match:
                        self.emission[j][i] = 1
                    prev_match = cur_match

            self.transition = np.ndarray((M, M), dtype="float")
            for i in range(M):
                for j in range(M):
                    s_i, s_j = self.state_map[i], self.state_map[j]
                    self.transition[i][j] = self.distr.posterior(s_i, s_j)

        else:
            raise ValueError("n-grams for n > 3 is not currently supported unfortunately.\
                    Use n = 2 or 3 in self.distr.")


    def viterbi(self):
        """
        Returns the word sequence to the MAP of the HMM,
        equivalent to finding the optimal path on trelli graph.

        Heavily and shamelessly inspired by (thanks in advance):
            https://stackoverflow.com/questions/9729968/python-implementation-of-viterbi-algorithm

        Parameters:
            y : array (M,)
                Observation state sequence. int dtype.
            A : array (K, K)
                State transition matrix. See HiddenMarkovModel.state_transition  for
                details.
            B : array (K, M)
                Emission matrix. See HiddenMarkovModel.emission for details.
            Pi: optional, (K,)
                Initial state probabilities: Pi[i] is the probability x[0] == i.
                If None, uniform initial distribution is assumed (Pi[:] == 1/K).

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
        A = self.transition . T
        B = self.emission . T
        K = A.shape[0]  # Cardinality of the state space
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
