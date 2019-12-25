DEFAULT_DICT = "sources/JPTable-iso.txt"


class JyutpingDict:
    def __init__(self, dict_path=DEFAULT_DICT):
        self.jyutdict = {}
        self.prefix_freq = {}
        self.suffix_freq = {}
        self.twoGram_freq = {}
        self.twoGramTail_freq = {}
        self.twoGramHead_freq = {}

        # Generate Dictionaries
        self._gen_jyutdict(file_path=dict_path)
        self._gen_prefixFreq()
        self._gen_suffixFreq()
        self._gen_twoGramFreq()

    def _gen_jyutdict(self, file_path):
        self.total = 0  # Number of entries in the dict
        with open(file_path) as f:
            for line_no, line in enumerate(f, 1):
                try:
                    utf_char, word, jyutping = line.split()[:3]
                    self.total += 1
                    if jyutping[:-1] not in self.jyutdict:
                        self.jyutdict[jyutping[:-1]] = [word]
                    else:
                        if word not in self.jyutdict[jyutping[:-1]]:
                            # In the case of jyutping differing by tone
                            self.jyutdict[jyutping[:-1]].append(word)
                except ValueError:
                    raise ValueError(
                        f"Invalid entry in {file_path} \
                        in line {line_no}"
                    )
        print(f"Dictionary of {len(self.jyutdict)} Jyutpings mapping to", \
                f"{self.total} different Chinese characters created")

    def _gen_prefixFreq(self):
        if self.jyutdict:
            for jyutping in self.jyutdict.keys():
                count = len(self.jyutdict[jyutping])
                if jyutping[0] not in self.prefix_freq:
                    self.prefix_freq[jyutping[0]] = count
                else:
                    self.prefix_freq[jyutping[0]] += count

    def _gen_suffixFreq(self):
        if self.jyutdict:
            for jyutping in self.jyutdict.keys():
                count = len(self.jyutdict[jyutping])
                if jyutping[-1] not in self.suffix_freq:
                    self.suffix_freq[jyutping[-1]] = count
                else:
                    self.suffix_freq[jyutping[-1]] += count

    def _gen_twoGramFreq(self):
        # Generates 2-gram frequencies
        if self.jyutdict:
            for jyutping in self.jyutdict.keys():
                twoGrams = [jyutping[idx:idx + 2] \
                            for idx in range(len(jyutping) - 1)]
                count = len(self.jyutdict[jyutping])

                if len(twoGrams) > 0:
                    # General 2-gram case
                    for tg in twoGrams:
                        if tg not in self.twoGram_freq:
                            self.twoGram_freq[tg] = count
                        else:
                            self.twoGram_freq[tg] += count

                    # Head 2-gram case
                    if twoGrams[0] not in self.twoGramHead_freq:
                        self.twoGramHead_freq[twoGrams[0]] = count
                    else:
                        self.twoGramHead_freq[twoGrams[0]] += count

                    # Tail 2-gram case
                    if twoGrams[-1] not in self.twoGramTail_freq:
                        self.twoGramTail_freq[twoGrams[-1]] = count
                    else:
                        self.twoGramTail_freq[twoGrams[-1]] += count

    def get_suggested_characters(self, jyutping):
        res = self.jyutdict[jyutping]
        return res if res else "None Found"

    def get_prefix_freq(self, prefix):
        freq = self.prefix_freq.get(prefix)
        return freq if freq else 0

    def get_suffix_freq(self, suffix):
        freq = self.suffix_freq.get(suffix)
        return freq if freq else 0

    def get_twoGramTail_freq(self, twoGram):
        freq = self.twoGramTail_freq.get(twoGram)
        return freq if freq else 0

    def get_twoGramHead_freq(self, twoGram):
        freq = self.twoGramHead_freq.get(twoGram)
        return freq if freq else 0

    def calc_twoGramTail_prob(self, twoGram):
        return self.get_twoGramTail_freq(twoGram) / self.total

    def calc_twoGramHead_prob(self, twoGram):
        return self.get_twoGramHead_freq(twoGram) / self.total

