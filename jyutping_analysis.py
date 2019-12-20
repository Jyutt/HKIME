# MIGRATE TO Jyupting Analysis.ipynb

DEFAULT_DICT="sources/JPTable-iso.txt"

class Jyutping:
    def __init__(self, dict_path=DEFAULT_DICT):
        self.jyutdict = {}
        self.prefix_freq = {}
        self.suffix_freq = {}
        self.gen_jyutdict(file_path=dict_path)
        self.gen_prefixFreq()
        self.gen_suffixFreq()

    def gen_jyutdict(self, file_path):
        self.total = 0
        with open(file_path) as f:
            for line_no, line in enumerate(f, 1):
                try:
                    utf_char, word, jyutping = line.split()[:3]
                    self.total += 1
                    if jyutping[:-1] not in self.jyutdict:
                        self.jyutdict[jyutping[:-1]] = [word]
                    else:
                        if word not in self.jyutdict[jyutping[:-1]]:
                            # In the case of jyutping differing only by tone 
                            self.jyutdict[jyutping[:-1]].append(word)
                except ValueError:
                    raise ValueError(
                        f"Invalid entry in {file_path} \
                        in line {line_no}"
                    )

    def gen_prefixFreq(self):
        if self.jyutdict:
            for jyutping in self.jyutdict.keys():
                count = len(self.jyutdict[jyutping])
                if jyutping[0] not in self.prefix_freq:
                    self.prefix_freq[jyutping[0]] = count
                else:
                    self.prefix_freq[jyutping[0]] += count
    
    def gen_suffixFreq(self):
        if self.jyutdict:
            for jyutping in self.jyutdict.keys():
                count = len(self.jyutdict[jyutping])
                if jyutping[-1] not in self.suffix_freq:
                    self.suffix_freq[jyutping[-1]] = count
                else:
                    self.suffix_freq[jyutping[-1]] += count 

    def get_suggested_characters(self, jyutping):
        res = self.jyutdict[jyutping]
        return res if res else "None Found"
    
    def get_prefix_freq(self):
        return self.prefix_freq
    
    def get_suffix_freq(self):
        return self.suffix_freq