# Correcting typos in a word based on the frequency dictionary.

import csv
import logging
from ScoreType import ScoreType
from typing import Dict

DICT_NAME = 'frequency_of_rus_words.csv'    # taken from http://dict.ruslang.ru/freq.php
LINEAR_COEFFICIENT = 500
POWER_COEFFICIENT = 10
EXPONENTIAL_COEFFICIENT = 10

CURRENT_SCORE_TYPE = ScoreType.EXPONENTIAL


def parse_dict(file_path: str) -> dict:
    """Take a vocabulary of frequency and bring it to the desired format

    :param file_path:
    :return:
    """

    result: Dict[str, float] = dict()
    with open(file_path, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter="\t")
        count = 0
        for row in file_reader:
            if count:
                result[row[0]] = float(row[2])
            count += 1
        logging.info(f'Found {count} words')
    return result


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    The source of this function:
    https://ru.wikipedia.org/wiki/Расстояние_Дамерау_—_Левенштейна

    :param s1:
    :param s2:
    :return:
    """
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1+1):
        d[(i, -1)] = i+1
    for j in range(-1, lenstr2+1):
        d[(-1, j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i-1, j)] + 1,
                d[(i, j-1)] + 1,
                d[(i-1, j-1)] + cost
            )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i-2, j-2] + 1)

    return d[lenstr1-1, lenstr2-1]


def calculate_score(algorithm_type: ScoreType, f: float, d: int) -> float:
    """Calculates points based on distance and word frequency. Calculates points based on distance and word frequency.
    Allows for the calculation function: LINEAR, POWER and EXPONENTIAL

    :param algorithm_type:
    :param f:
    :param d:
    :return:
    """

    functions_by_type = {
        ScoreType.LINEAR: (lambda f, d: f/(1 + (d-1)*LINEAR_COEFFICIENT)),
        ScoreType.POWER: (lambda f, d: f/(d**POWER_COEFFICIENT)),
        ScoreType.EXPONENTIAL: (lambda f, d: f/(EXPONENTIAL_COEFFICIENT**d)),
    }

    return functions_by_type[algorithm_type](f, d)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    frequency = parse_dict(DICT_NAME)
    current_word = input('Enter a word: ')
    if current_word in frequency:
        print(f'The word "{current_word}" is written without typos.')
    else:
        best_score, close_word = 0, str()
        for word, freq in frequency.items():
            dist = damerau_levenshtein_distance(current_word, word)
            score = calculate_score(CURRENT_SCORE_TYPE, freq, dist)
            if score > best_score:
                best_score, close_word = score, word
                logging.debug(f'word: {word}, distance: {dist}, frequency: {freq}, score: {score}')
        print(f'Maybe you meant "{close_word}"?')