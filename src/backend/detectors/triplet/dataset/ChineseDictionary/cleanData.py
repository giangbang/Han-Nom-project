import re

def clean_input_characters(args):
	lines = []
	with open(args.data_file_name, 'r', encoding="utf-8") as f:
		lines = f.readlines()

	lines = [ln.strip() for ln in lines]
	words = u''.join(lines)
	
	print('Total length of the original data: {} characters'.format(len(words)))
	if args.exclude_alphabet:
		words = filter(lambda x: not x.encode('utf-8').isalpha(), words)
	if args.exclude_number:
		words = filter(lambda x: not x.encode('utf-8').isdigit(), words)
	if args.unique:
		words = u''.join(set(words))
	# remove general special characters
	words = re.sub('/[^\u4E00-\u9FFF]+/u', '', words)
	print("Total length of the processed data: {} characters".format(len(words)))
	
	with open(args.output_file_name, 'w', encoding='utf-8') as f:
		f.write(words)
		
if __name__ == '__main__':
	import argparse
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('--data_file_name', '--in', type=str, 
						default='./chinese-word-list.txt',
                        help='Name of data file need to be cleaned')
						
	parser.add_argument('--output_file_name', '--out', type=str, 
						default='./cleaned-chinese-word-list.txt',
                        help='Name of output file')					
						
	parser.add_argument('--exclude_alphabet', '--alb', type=bool, 
						default=True,
                        help='Whether to exclude alphabet characters or not')
	
	parser.add_argument('--exclude_number', '--num', type=bool, 
						default=True,
                        help='Whether to exclude number characters or not')
	
	parser.add_argument('--unique', '--unq', type=bool, 
						default=True,
                        help='Whether to eliminate identical characters or not')
						
	args = parser.parse_args()
	clean_input_characters(args)