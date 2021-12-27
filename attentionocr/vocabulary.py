import string

import numpy as np


# default_vocabulary = list(string.ascii_lowercase) + list(string.digits) + [' ', '-', '.', ':', '?', '!', '<', '>', '#', '@', '(', ')', '$', '%', '&']
default_vocabulary = ["آ", "ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر","ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک","گ", "ل", "م", "ن", "و", "ه", "ی"]

class Vocabulary:
    pad = '<PAD>'
    sos = '<SOS>'
    eos = '<EOS>'
    unk = '<UNK>'

    def __init__(self, vocabulary: list = default_vocabulary):
        self._characters = [self.pad, self.sos, self.eos, self.unk] + sorted(vocabulary)
        self._character_index = dict([(char, i) for i, char in enumerate(self._characters)])
        self._character_reverse_index = dict((i, char) for char, i in self._character_index.items())

    def is_special_character(self, char_idx):
        return self._characters[char_idx] in [self.pad, self.sos, self.eos]

    def one_hot_encode(self, txt: str, length: int, sos: bool = False, eos: bool = True) -> np.ndarray:
        txt = list(txt)
        txt = txt[:length - int(sos) - int(eos)]
        txt = [c if c in self._characters else self.unk for c in txt]
        if sos:
            txt = [self.sos] + txt
        if eos:
            txt = txt + [self.eos]
        txt += [self.pad] * (length - len(txt))
        encoding = np.zeros((length, len(self)), dtype='float32')
        for char_pos, char in enumerate(txt):
            if char in self._character_index:
                encoding[char_pos, self._character_index[char]] = 1.
            else:
                encoding[char_pos, self._character_index[self.unk]] = 1.
        return encoding

    def one_hot_decode(self, one_hot: np.ndarray, max_length: int) -> str:
        text = ''
        for sample_index in np.argmax(one_hot, axis=-1):
            sample = self._character_reverse_index[sample_index]
            if sample == self.eos or sample == self.pad or len(text) > max_length:
                break
            text += sample
        return text

    def __len__(self):
        return len(self._characters)
