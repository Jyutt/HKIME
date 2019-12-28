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
                //pinyin to character

            distr: Dictionary representing trigram distribution
                (maybe we need to create a distribution class?
                // do this later

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
                    // tokenized pinyin e.g. ['pin', 'yin'....]
					// assume there exists: def match() that returns list of kanto words, e.g. ['我'， ‘是’，。。。]
        """

    def viterbi(self, obsspace, statespace, initprobs, observations, transition, emission):
        """
        Finds the optimal path in the graph, which is equivalent to
        predicting the most likely sentence / phrase given the Jyutping list

        Use Viterbi? Yes

		-----Prototype (2-grams, dependant on only i-1 state where i is current state)----
        Example: 我是新藏人

        @params
        	-obsspace: a list of all possible observations O = {o_1, o_2, ..., o_N}

			-statespace: the state space S = {s_1, s_2, ..., s_k}, a sequence of k states 
			(what is k in this example?)

			-initprobs: an array of initial probabilities ∏ = (π_1, π_2, ... π_k)
			s.t. π_i = Pr(x_1 = s_i) (so the |S| = k in this case should = the # of characters
			‘wo’ can take on?)

			-observations: a sequence of observations/predictions Y = (y_1, y_2, ..., y_T)
			s.t. (Observation at time t = o_i) => (y_t == i) 

			-transition: a matrix A of size K x K s.t. 
			A_ij = Pr(transiting from s_i to s_j). This input should be taken from the trained
			probabilities Pr(w_i | w_i-1 union w_i-2)

			-emission matrix: a matrix B of size K x N s.t.
			B_ij = Pr(observing o_j from state s_i)

		@returns
			-most likely hidden state sequence X = (x_1, x_2, ..., x_T)
        """

        # initialize lengths
        K = len(statespace)  # = len(initprobs)
        T = len(observations)
        # construct two K x T matricies (all entries initialized to 0)
        M1 = [[0 for j in range(T)] for i in range(K)]
        M2 = [[0 for j in range(T)] for i in range(K)]
        # construct return sequence
        X = [0 for i in range(T)]

        for i in range(K):      # for each state in state space
        	M1[i, 1] = initprobs[i] * emission[i, observations[1]]
        	M2[i, 1] = 0
        for i in range(1, T):   # for each non-initial observation
        	for j in range(K):  # for each state in state space

        		# an array of "M1[k, j-1] * A_ki * B_ix" for all k, where x = y_j
        		temparr = [M1[k, j - 1] * transition[k, i] * emission[i, observations[j]] for k in range(K)]
        		M1[i, j] = max(temparr)               # max of temparr
        		M2[i, j] = temparr.index(M1[i, j])    # argmax of temparr


        ### ---back tracking stage--- ###

        # an array of "M1[k, T-1]" for all k 
        temparr = [M1[k, T - 1] for k in range(K)]
        argmax_arr = [0 for i in range(T)]               # intermediate array
        argmax_arr[T - 1] = temparr.index(max(temparr))  # set last element of argmax_arr to argmax(temparr)

        X[T - 1] = statespace[argmax_arr[T - 1]]         # (put more informative comments)

        for i in reversed(range(T)):  # for each col in M2 (counting in reverse order)
        	argmax_arr[i - 1] = M2[argmax_arr[i], i]
        	X[i - 1] = statespace[argmax_arr[i - 1]]

        return X




