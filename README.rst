About
=====

Simple but effective script for cleaning parallel corpora based on dictionary and stop words.

Usage
=====

 Script count two numbers:
    m - total number of words in sentence (excluding stop words)
    n - total number of words in sentence from dictionary
Filtering can be done using absolute and relative difference:
    abs_diff = n
    rel_diff = n/m
Sentence will be preserved if absolute or relative difference is more for it
then provided in script options

Example command:
    $ python sentence_cleaner.py --abs_diff 3 --dictionary dictionary.txt --stop_words stop.txt text1 text2

Cleaned sentences will be saved as "cleaned__[file_name]"


Final info
====

Feel free to use this tool if you cite:
•	Wołk K., Marasek K., “Unsupervised comparable corpora preparation and exploration for bi-lingual translation equivalents”, Proceedings of the 12th International Workshop on Spoken Language Translation, Da Nang, Vietnam, December 3-4, 2015, p.118-125

For more information, see: http://arxiv.org/pdf/1512.01641

For any questions:
| Krzysztof Wolk
| krzysztof@wolk.pl