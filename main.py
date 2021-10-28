import itertools as it

# Paste here the data file's path
filePath = "data.txt"

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

class Account:
	def __init__(self, line0: list, line1: list, line2: list):
		self.raw_data = [
			line0,
			line1,
			line2
		]

		self.possibilities = []

		self.account_number = self.convertDigitsToHex()

		if self.isValid() and '?' not in self.account_number:
			self.status = None
		elif not self.isValid() and '?' in self.account_number:
			self.status = "ILL"
		else:
			self.status = "ERR"
	
		if self.status == "ILL":
			self.account_number, self.status, self.possibilities = self.guessILL()
		if self.status == "ERR":
			self.account_number, self.status, self.possibilities = self.guessERR()
	
	def __str__(self) -> str:
		"""
		On call of the instace it returns its values in a formated way.
		"""
		return f"{self.account_number}{f' {self.status}' if self.status is not None else ''}{f' {self.possibilities}' if self.possibilities else ''}"
	
	def getDigit(self, n: int, raw_data: list=None) -> list:
		"""
		Gets its n-th term as underscores and pipes.
		"""
		if raw_data is None:
			raw_data = self.raw_data

		digit = [
			[],
			[],
			[]
		]
		for character in range(n*4, n*4+4):
			for index, line in enumerate(raw_data):
				digit[index].append(line[character])

		return digit

	def convertDigitsToHex(self, raw_data: list=None) -> str:
		"""
		Converts the digits from underscores and pipes to integers.
		"""
		if raw_data is None:
			raw_data = self.raw_data

		account_number = ""
		
		for nth_term in range(round(len(raw_data[0])/4)):
			for index in range(len(digit_matrix)+1):
				if self.getDigit(nth_term) == digit_matrix[index]:
					account_number += str(format(index, 'x').upper())
					break
				else:
					if index != len(digit_matrix)-1:
						continue
					else:
						account_number += "?"
						break

		return account_number

	def isValid(self, account_number: str=None) -> bool:
		"""
		Validates an account number. If the checksum is right it returns True.
		"""
		if account_number is None:
			account_number = self.account_number
		
		checksum = 0
		for index, number in enumerate(account_number[::-1]):
			if number == '?':
				return False
				
			checksum += (index + 1) * int(number, 16)
		
		if checksum % 11 == 0:
			return True
		else:
			return False

	def bruteForceDigits(self, index: int, raw_data: list=None) -> (int, str):
		"""
		Gets every possible "mistakes" that could occur and returns the valid ones.
		"""
		if raw_data == None:
			raw_data = self.raw_data

		all_symbols = [' ', '|', '_', '\\', '/']

		# copy digit at a given index
		base = [[],[],[]]
		for y in range(3):
			for x in range(index*4, index*4+4):
				base[y].append(raw_data[y][x])
		
		# brute force the possible digits
		number = []
		for nth_digit in range(16):
			for y in range(3):
				for x in range(4):
			
					# ' '
					if (y == x == 0) or (y ==  0 and x == 2) or x == 3:
						continue
					
					# ' ', '_'
					if x == 1:
						symbols = [all_symbols[0], all_symbols[2]]
			
					# ' ', '|'
					elif y >= 1 and x == 0:
						symbols = [all_symbols[0], all_symbols[1]]
			
					# ' ', '|', '\', '/'
					elif y >= 1 and x == 2:
						symbols = [all_symbols[0], all_symbols[1], all_symbols[3], all_symbols[4]]

					og_symbol = base[y][x]

					for s in symbols:
						if s != base[y][x]:
							base[y][x] = s

						if base == digit_matrix[nth_digit] and nth_digit not in number:
							number.append(nth_digit)
						base[y][x] = og_symbol
		if number:
			return number
		else:
			return None

	def combinator(self, digits: dict, account_number: str=None) -> str:
		"""
		Creates the possible combinations for the ILL statused account number(s) and
		returns the valid one(s) in the right format.
		"""
		if account_number is None:
			account_number = self.account_number
		
		# Creates every combinations
		combinations = it.product(*(digits[digit] for digit in digits))
		
		# Complies every account number and validates them
		indexes = list(x for x in digits)
		solutions = []
		for combination in combinations:
			tmp_account_number = account_number

			for i, index in enumerate(indexes):
				tmp_account_number = tmp_account_number[:index] + str(combination[i] if combination[i] < 10 else['A', 'B', 'C', 'D', 'E', 'F'][combination[i]-10]) + tmp_account_number[index+1:]
			
			if self.isValid(account_number=tmp_account_number):
				solutions.append(tmp_account_number)
			
		return solutions
		
	def guessERR(self, raw_data: list=None) -> (str, str, list):
		"""
		Tries to guess which ERR statused account number is misread and corrects it if possible.
		"""
		if raw_data is None:
			raw_data = self.raw_data
		
		account_number = self.convertDigitsToHex(raw_data)
		
		# Get the possible digits
		digits = {}
		for index in range(len(account_number)):
			digits[index] = self.bruteForceDigits(index=index, raw_data=raw_data)
			if digits[index] is None:
				return account_number, "ERR", []
		
		# Compiles and verifies the possibilities
		solutions = []
		for digit in digits:
			for d in digits[digit]:
				possibility = account_number
				possibility = possibility[:digit] + str(d if d < 10 else['A', 'B', 'C', 'D', 'E', 'F'][d-10]) + possibility[digit+1:]
				
				if self.isValid(possibility):
					solutions.append(possibility)

		# Returns the valid account number(s) in the right format
		if solutions:
			if len(solutions) == 1:
				return solutions[0], None, []
			else:
				return account_number, "AMB", solutions
		else:
			return account_number, "ERR", []

	def guessILL(self, raw_data: list=None) -> (str, str, list):
		"""
		Tries to correct the ILL statused account numbers
		"""
		if raw_data is None:
			raw_data = self.raw_data
		
		account_number = self.convertDigitsToHex(raw_data)

		# Getting the indexes of illegible digits
		ills = []
		
		for i, char in enumerate(account_number):
			if char == '?':
				ills.append(i)
		
		
		# Get the possible digits
		digits = {}
		for index in ills:
			digits[index] = self.bruteForceDigits(index=index, raw_data=raw_data)
			if digits[index] is None:
				return account_number, "ILL", []
		
		# Get the good account numbers
		solutions = self.combinator(digits=digits, account_number=account_number)

		if solutions:
			if len(solutions) == 1:
				return solutions[0], None, []
			else:
				return account_number, "AMB", solutions
		else:
			return account_number, "ILL", []	


if __name__ == "__main__":
	accounts = []
	# Open and read the data file
	with open(filePath, 'r', encoding="utf-8") as f:
		data = f.readlines()
		
		# Iterate through the file's lines
		for index in range(len(data)):

			# Get every 3 lines
			if index % 3 == 0:
				line0 = data[index].replace("\n", "")
			elif index % 3 == 1:
				line1 = data[index].replace("\n", "")
			else:
				line2 = data[index].replace("\n", "")
				accounts.append(Account(line0, line1, line2))

		for account in accounts:
			print(account)