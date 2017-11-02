"""
Transliterate module for converting from one symbol set to another.
Originally written for transliteration between Serbian Latin and Cyrillic alphabet.
"""

__author__ = 'Dejan Vesić, Dejan@Vesic.Org'
__version__ = '0.1.0'
__license__ = 'MIT'

import os
import sys
import argparse
import configparser


def transliterate(line, trans_dict):
    """
    Core function for transliteration of one line, one word at time

    :param line: source string line for transliteration
    :param trans_dict: transliteration instructions via 4 dictionaries
    :return: transliterated string
    """

    words = line.split()
    new_words = []
    for word in words:
        for key, value in trans_dict["Double"].items():
            word = word.replace(key, value)
        letters = list(word)
        new_word = ''

        for letter in letters:
            new_word += trans_dict["Single"].get(letter, letter)

        for key, value in trans_dict["Partial"].items():
            new_word = new_word.replace(key, value)

        new_word = trans_dict["Replace"].get(new_word, new_word)

        new_words.append(new_word)

    return " ".join(new_words)


def read_config(ini_file):
    """
    :param ini_file: path to INI file, with transliteration rules
    :return: dictionary of four dictionaries, created over INI file
    """
    config = configparser.ConfigParser()

    # We need case-sensitive options in INI file
    config.optionxform = str

    # Also INI file should be in UTF8
    fh_ini = open(ini_file, "r", encoding="utf8")
    config.read_file(fh_ini)

    double = {}
    if config.has_section("Double"):
        double = dict(config.items("Double"))

    single = {}
    if config.has_section("Single"):
        single = dict(config.items("Single"))

    fb_partial = {}
    if config.has_section("Fallback-Partial"):
        fb_partial = dict(config.items("Fallback-Partial"))

    fb_whole = {}
    if config.has_section("Fallback-Whole"):
        fb_whole = dict(config.items("Fallback-Whole"))

    return {
            "Double": double,
            "Single": single,
            "Partial": fb_partial,
            "Replace": fb_whole
            }


def trans_file(ini_file, in_text, out_file):
    """
    Helper function for processing files from command line

    :param ini_file: transliteration instructions
    :param in_text: source file for transliteration
    :param out_file: (optional) target file for transliterated text
    :return: Exit code - 0 for all OK, others depending on the error

    Errors:
        0   Success. All OK
        -1  ini_file does not exist
        -2  in_text file does not exist
        -3  in and out file same
        -100 Minimal python version not satisfied
    """

    # Due to support of path.samefile on Windows platform
    if sys.version_info < (3, 2):
        return -100

    if not os.path.isfile(ini_file):
        return -1

    if not os.path.isfile(in_text):
        return -2

    is_stdout = False

    if out_file == "stdout":
        file = sys.stdout
        is_stdout = True
    else:
        if os.path.isfile(out_file):
            if os.path.samefile(in_text, out_file):
                return -3
        file = open(out_file, "w", encoding="utf8")

    # Real work

    trans_dict = read_config(ini_file)

    with open(in_text, "r", encoding="utf8") as fh_in:
        for line in fh_in.readlines():
            print(transliterate(line, trans_dict), file=file)

    if not is_stdout:
        file.close()

    return 0


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("ini_file", help="Ini file with transliteration instructions")
    parser.add_argument("-i", "--in-file", action="store", dest="in_text", help="File with original symbol set text")
    parser.add_argument("-o", "--out-file", action="store", dest="out_file", default="stdout",
                        help="File where to write transliterated text, default is stdout")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    result = trans_file(args.ini_file, args.in_text, args.out_file)
    print("Result code is {}".format(result))
