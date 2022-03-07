`ChineseDictionary` is a module for storing all Chinese characters used in the training process.

First, a dictionary of common Chinese words used is collected in the `chinese-word-list.txt` file. This file might contain undesired characters like alphabet strings, numbers, EOF etc and need to be cleaned. 

The data cleaning process can be reproduced by running `python cleanData.py --in <input> --out <output>` or just simply `python cleanData.py`. By default, the result will be saved at `cleaned-chinese-word-list.txt`.
