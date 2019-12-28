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

		-----Prototype (2-grams, dependant on only i-1 state where i is current state)-----
        Example: Observed string:            wo shi xi zang ren 
        		 Optimal character string:   我  是  西  藏   人

        @params

        -obsspace: a list of all possible observations O = {o_1, o_2, ..., o_N}
        	From this example, N = 5 since we can only observe 'wo' from all characters that are pronounced as 'wo',
        	and similarly for all other characters in the input pinyin/observation string.
        	In other words, theres only one possible observation from 我, one from 是, etc.
			
			CHECK NOTE 1 FOR EXPLANATION ON KANTO PINYIN AMBIGUITY


		-statespace: the state space S = {s_1, s_2, ..., s_k}, a sequence of k states 
			In this example, S would be contain the possible characters 我 can take + 
												the possible characters 是 can take + ...
											 ...the possible characters 人 can take


		-initprobs: an array of initial probabilities ∏ = (π_1, π_2, ... π_k) s.t. π_i = Pr(x_1 = s_i)
			In this example, Pr(x_1 = s_i) ≠ 0 for all s_i that is a character with a pinyin 'wo', 
						 and Pr(x_1 = s_i) = 0 otherwise 
			(basically, the first pinyin/observation, or 'wo' should have no probability in being a
			character like 心，人，仁 etc. This is a memory space loss we have to cope with since the 
			state space for each of our observations/pinyin are different, e.g. 
				'wo''s state space is  {'我', '握', '喔', ...} and
				'shi''s state space is {'是', '师', '时', ...})


		-observations: a sequence of observations/predictions Y = (y_1, y_2, ..., y_T)
			s.t. (Observation at time t = o_i) => (y_t == i) 
			A trivial matrix for this application, since the observation doesn't change over time, 
			hence y_j = y (See the description for the emission matrix for more clarification).
			So for this example, Y = (1, 2, 3, 4, 5)
			
			CHECK NOTE 2 ON INDEXING ISSUES


		-transition: a matrix A of size K x K s.t. 
			A_ij = Pr(transiting from s_i to s_j). This input should be taken from the trained
			probabilities Pr(w_i | w_i-1) for 2-grams, or Pr(w_i | w_i-1 union w_i-2) for trigrams 

			For simplicity, I will consider conditions for two separate cases:

			Case 1, all observations are distinct (e.g. {'wo', 'shi', 'xi', 'zang', 'ren'}, {'huan', 'ying', 'ni'}):
				In this case, s_ij ≠ 0 when i = j + 1, and
						      s_ij = 0 otherwise,      
				i.e. there is some chance that 
				state s_i transitions to s_j where j = i + 1 (e.g. the next character after 我 is 
				something pronounced 'shi'), and there is no chance otherwise (我 will never transition to 
				something pronounced e.g. 'xi' or 'ren' etc.), since the input already defines the order of 
				observations, hence there is no ambiguity when it comes to when we observe what. 

				The probabilities in the first condition will come from the language model that is supposed
				to learn how likely it is for a specific character to follow another (or to follow a term of two
				characters for trigrams)


			Case 2, there exist duplicate observations in the observed string, i.e. |O| = N < len(observed string)
			(e.g. {'wo', 'wo', 'zhu', 'le', 'fu', 'shou'} (我握住了扶手）, {'pi', 'tu', 'pi'} (匹凸匹)):
				This example contains more probabilities as e.g. for the second example, 匹 can transit to 
				凸 and vice versa. Like the first case however, the probabilities will all be handeled by the
				languange model.


		-emission matrix: a matrix B of size K x N s.t. B_ij = Pr(observing o_j from state s_i)
			A trivial matrix in this application. For this example, the matrix basicaly looks like:

			[[Pr(Observing 'wo' from  ‘我’), Pr(Observing 'shi' from ‘我’), ..., Pr(Observing 'ren' from ‘我’)],
			 [Pr(Observing 'wo' from  ‘握’), Pr(Observing 'shi' from ‘握’), ..., Pr(Observing 'ren' from ‘握’)],
			 ...
			 [Pr(Observing 'wo' from  ‘是’), Pr(Observing 'shi' from ‘是’), ..., Pr(Observing 'ren' from ‘是’)],
			 [Pr(Observing 'wo' from  ‘师’), Pr(Observing 'shi' from ‘师’), ..., Pr(Observing 'ren' from ‘师’)],
			 ...
			 [Pr(Observing 'wo' from  ‘人‘), Pr(Observing 'shi' from ‘人’), ..., Pr(Observing 'ren' from ‘人’)]]

			which is just an array of a bunch of one hot vectors:

			[[1, 0, 0, ..., 0],
			 [1, 0, 0, ..., 0],
			 ...
			 [0, 1, 0, ..., 0],
			 [0, 1, 0, ..., 0],
			 ...
			 [0, 0, 0, ..., 1]]


		@returns
			-most likely hidden state sequence X = (x_1, x_2, ..., x_T)


		NOTES:

		    1: (THIS MIGHT NOT BE THE CASE FOR KANTO PINYIN, SINCE I HEARD SOME CHARACTERS CAN BE 
        	REPRESENTED WITH DIFFERENT PINYIN STRINGS. BUT ANYWAYS, WE'RE ONLY PREDICTING THE CHARACTER 
        	STRING IN THE END, SO WHAT PINYIN WE USE TO REPRESENT THAT CHARACTER DONT MATTER, i.e. 
        	observing 'wo' from 我 or 'weh' from it doesn't make a difference when we just want 我 anyways)
			cOrReCt mE iF Im wrOnG

			2: INDEXING IN THE ABOVE EXAMPLES ALL START FROM 1 AND GOES TO THE LENGTH, BUT IN PRACTICE (CODE)
			ALL INDEXES START FROM 0 AND GOES TO LENGTH - 1, so Y = (0, 1, 2, 3, 4) in reality

        """

        # initialize lengths
        K = len(statespace)  # = len(initprobs)
        T = len(observations)
        # construct two temporary K x T matricies (all entries initialized to 0)
        M1 = [[0 for j in range(T)] for i in range(K)]
        M2 = [[0 for j in range(T)] for i in range(K)]
        # construct return sequence
        X = [0 for i in range(T)]

        for i in range(K):                            # for each state in state space
        	M1[i, 1] = initprobs[i] * emission[i, observations[1]]
        	M2[i, 1] = 0
        for i in range(1, T):                         # for each non-initial observation
        	for j in range(K):                        # for each state in state space

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

        for i in reversed(range(T)):                     # for each col in M2 (counting in reverse order)
        	argmax_arr[i - 1] = M2[argmax_arr[i], i]
        	X[i - 1] = statespace[argmax_arr[i - 1]]

        return X


