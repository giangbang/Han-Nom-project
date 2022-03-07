import os

import sys

def get_allCharacters():
	allCharacters = []
	sys.path.append(os.path.dirname(os.path.realpath(__file__)))

	dir_path = os.path.dirname(os.path.realpath(__file__))
	chinese_dict_path = os.path.join(dir_path, 'cleaned-chinese-word-list.txt')
	print('Reading list of Chinese Characters used for inference...')
	with open(chinese_dict_path, 'r', encoding="utf-8") as f:
		allCharacters = f.readlines()[0]
	print('Done')
	return allCharacters
	

