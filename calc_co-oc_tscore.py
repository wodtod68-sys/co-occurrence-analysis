#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):

    freqs = {}

    for line in open(filename, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        freqs[parts[0]] = int(parts[1])

    return freqs

###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):

    t_scores = {}

    for line in open(filename, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue

        word1, word2, cofreq = parts[0], parts[1], int(parts[2])

        # 공기빈도가 CUTOFF 이상인 경우만 계산
        if cofreq < cutoff:
            continue

        # 2gram은 정렬된 쌍을 한 번만 저장하므로 양방향 모두 계산
        for target, coword in [(word1, word2), (word2, word1)]:

            # 대상어가 공기어를 포함하면 출력하지 않음 (예: 개인정보/정보)
            if coword in target:
                continue

            observed = cofreq
            expected = unigram_context[target] * unigrams[coword] / uni_N
            t = (observed - expected) / math.sqrt(observed)

            # t-점수가 양수인 경우만 출력
            if t > 0:
                t_scores[(target, coword)] = t

    return t_scores

###############################################################################
def print_tscore(filename, t_scores):

    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        for (target, coword) in sorted(t_scores):
            f.write(f"{target}\t{coword}\t{t_scores[(target, coword)]:.3f}\n")

###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:

        print(f"processing {input_file}", file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"

        print(f"\tLoading {file_stem}.1gram", file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")

        print(f"\tLoading {file_stem}.1gram_context", file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")

        uni_N = unigrams['#Total'] # unigram 빈도 합

        # key : (target, coword)
        # value : t-score
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)

        print_tscore(file_stem+".tscore", t_scores)
