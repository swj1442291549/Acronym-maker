import re
import itertools

import regex

from rich import print


def get_words_list():
    with open("./wiki-100k.txt", 'r') as f:
        words = f.readlines()

    return words

def gen_pattern(words_list):
    pattern = list()
    for word in words_list:
        if word.islower():
            pattern.append(word[0] + "?" if "?" in word else word[0])
        else:
            for i, char in enumerate(word):
                if char.isupper() or i == 0:
                    pattern.append(char.lower())
        pattern.append("[a-z]{0,2}")
    pattern = "".join(pattern)
    pattern = "".join(["^a?", pattern, "$"])
    return pattern

def gen_query_pattern(words_list, index):
    pattern = list()
    for j, word in enumerate(words_list):
        if j == index:
            pattern.append(")")
        if word.islower():
            pattern.append(word[0] + "?" if "?" in word else word[0])
        else:
            for i, char in enumerate(word):
                if char.isupper() or i == 0:
                    pattern.append(char.lower())
        if j == index:
            pattern.append("(?=")
        pattern.append("[a-z]{0,2}")
    pattern = "".join(pattern)
    pattern = "".join(["(?<=a?", pattern, ")"])
    return pattern

def format_print(result, words_list):
    result_list = list(result)
    for i in range(len(words_list)):
        pattern = gen_query_pattern(words_list, i)
        span = regex.search(pattern, result).span()
        result_list.insert(2 * i + span[0], "[Bold magenta]")
        result_list.insert(2 * i + span[1] + 1, "[/Bold magenta]")
    print("".join(result_list))


if __name__ == "__main__":
    words = get_words_list()

    # query_words = input()
    query_words = "Virgo Environmental Survey Tracing Ionised Gas Emission"
    query_words = "OpenCluster Rotation survey population member?"

    query_words_list = query_words.strip().split(' ')

    for permutation in list(itertools.permutations(query_words_list)):
        pattern = gen_pattern(permutation)

        prog = re.compile(pattern, flags=re.M)
        results = prog.findall(''.join(words))
        if len(results) != 0:
            print(permutation)
            for result in results:
                format_print(result, permutation)

