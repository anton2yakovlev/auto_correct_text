# This is a sample Python script.

import csv
import logging
from typing import Dict

DICT_NAME = 'frequency_of_rus_words.csv'


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    frequency = parse_dict(DICT_NAME)



