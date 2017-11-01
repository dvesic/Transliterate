# Transliterate
Python transliterate module for converting from one symbol set to another. Originally written for transliteration between Serbian Latin and Cyrillic alphabet.

## Transliterate instructions

This is contained in four dictionaries: *Double*, *Single*, *Fallback-Partial* and *Fallback-Whole* and processed exactly in that order.

### Double

Some letters in Serbian alphabet are represented as two-letter in Latin script. For example: Nj -> Њ 

This table does exactly that - translates two letters from source file to particular letter in target file. Used for Latin -> Cyrillic transliteration.

### Single

Simplest part - translation from particular letter from source file to particular letter in target file.

### Fallback-Partial

In some cases, two set of rules above won't produce correct result, usually due to [conjugation rules](https://en.wikipedia.org/wiki/Grammatical_conjugation). This aims to correct that, by annulating wrongly transliterated parts of the word.

### Fallback-Whole

Finally, this section is for words which should stay non-modified (like foreign words or brands).

## Usage

Module can be used from command line, supplying at least two files as a parameter:

- INI file with transliteration rules
- Input text file for transliteration

*Example*:

py Transliterate.py lat2cir.ini -i latinica.txt -o cirilica.txt

## Credits

Many thanks to [Aleksandar Urošević](https://twitter.com/urosevic) for initial help in creating this module!
