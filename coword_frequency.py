#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations

###############################################################################
def print_word_freq(filename, word_freq):

    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        # #Total은 첫 줄에 먼저 출력 (1gram에만 존재)
        if "#Total" in word_freq:
            f.write(f"#Total\t{word_freq['#Total']}\n")

        for word in sorted(w for w in word_freq if w != "#Total"):
            f.write(f"{word}\t{word_freq[word]}\n")

###############################################################################
def print_coword_freq(filename, coword_freq):

    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        for (target, coword) in sorted(coword_freq):
            f.write(f"{target}\t{coword}\t{coword_freq[(target, coword)]}\n")

###############################################################################
def get_coword_freq(filename):

    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)
    word_freq = defaultdict(int)
    total_unigram_count = 0

    for line in open(filename, encoding="utf-8"):
        # 같은 문맥에서 반복 출현하는 단어는 1번으로 간주 (집합으로 중복 제거)
        words = set(line.split())
        if not words:
            continue

        context_size = len(words)
        total_unigram_count += context_size

        for word in words:
            word_freq[word] += 1
            word_context_size[word] += context_size

        # 정렬된 단어쌍을 한 번만 (target < coword)
        for target, coword in combinations(sorted(words), 2):
            coword_freq[(target, coword)] += 1

    word_freq["#Total"] = total_unigram_count

    return word_freq, coword_freq, word_context_size

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:

        print(f"processing {input_file}", file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "2017"

        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1gram", word_freq)

        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_context", word_context_size)
