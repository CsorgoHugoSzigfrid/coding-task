import random, argparse, math

"""

For help please run "py GenTestFile.py -h or --help"

"""

parser = argparse.ArgumentParser(description="Generates a given amount of test data randomly with every type of account numbers.")
parser.add_argument("-l", "--length", help="Sets the length of an account number", type=int)
parser.add_argument("-d", "--dataset_size", help="Sets the max amount of data.", type=int)
        
args = parser.parse_args()


length = 9
dataset_size = 500


if args.length:
	if args.length < 4:
		length = 4
	else:
		length = args.length
if args.dataset_size:
	if args.dataset_size < 4:
		dataset_size = 4
	else:
		dataset_size = math.floor(args.dataset_size/4)*4


digit_matrix = {
	0: [[' ', '_', ' ', ' '], ['|', ' ', '|', ' '], ['|', '_', '|', ' ']],
    1: [[' ', ' ', ' ', ' '], [' ', ' ', '|', ' '], [' ', ' ', '|', ' ']],
    2: [[' ', '_', ' ', ' '], [' ', '_', '|', ' '], ['|', '_', ' ', ' ']],
    3: [[' ', '_', ' ', ' '], [' ', '_', '|', ' '], [' ', '_', '|', ' ']],
    4: [[' ', ' ', ' ', ' '], ['|', '_', '|', ' '], [' ', ' ', '|', ' ']],
    5: [[' ', '_', ' ', ' '], ['|', '_', ' ', ' '], [' ', '_', '|', ' ']],
    6: [[' ', '_', ' ', ' '], ['|', '_', ' ', ' '], ['|', '_', '|', ' ']],
    7: [[' ', '_', ' ', ' '], [' ', ' ', '|', ' '], [' ', ' ', '|', ' ']],
    8: [[' ', '_', ' ', ' '], ['|', '_', '|', ' '], ['|', '_', '|', ' ']],
    9: [[' ', '_', ' ', ' '], ['|', '_', '|', ' '], [' ', '_', '|', ' ']],
	10: [[' ', '_', ' ', ' '], ['|', '_', '|', ' '], ['|', ' ', '|', ' ']],
    11: [[' ', '_', ' ', ' '], ['|', '_', '\\', ' '], ['|', '_', '/', ' ']],
	12: [[' ', '_', ' ', ' '], ['|', ' ', ' ', ' '], ['|', '_', ' ', ' ']],
    13: [[' ', '_', ' ', ' '], ['|', ' ', '\\', ' '], ['|', '_', '/', ' ']],
    14: [[' ', '_', ' ', ' '], ['|', '_', ' ', ' '], ['|', '_', ' ', ' ']],
    15: [[' ', '_', ' ', ' '], ['|', '_', ' ', ' '], ['|', ' ', ' ', ' ']]
}

if __name__ == "__main__":
	with open("data.txt", mode='w+', encoding="utf-8") as f:
		for i in range(dataset_size):
			digits = [
				[],
				[],
				[]
			]

			# Create digits as lists
			account_number = []
			for d in range(length):
				account_number.append(str(random.choice(list(digit_matrix.keys()))))
			
			checksum = 0
			for index, number in enumerate(account_number[::-1]):
				
				checksum += (index + 1) * int(number, 16)
			
			# Randomly changes a character
			if random.choice([True, False]):
				digit = random.choice([x for x in digit_matrix])
				account_number[random.choice(range(length))] = digit

			for n in account_number:
				for row in range(3):
					for col in range(4):
						if random.choices([True, False], weights=(97, 3), k=1)[0]:
							digits[row].append(digit_matrix[int(n)][row][col])
						else:
							digits[row].append(' ')


			# Convert lists to strings AND write it to the data.txt file.
			for x in digits:
				str1 = ""
				for y in x:
					str1 += y

				f.write(f"{str1}\n")