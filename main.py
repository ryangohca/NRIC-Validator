"""
Steps:
1) Take for example I want to test the NRIC number S1234567. The first digit
   you multiply by 2, second multiply by 7, third by 6, fourth by 5, 
   fifth by 4, sixth by 3, seventh by 2. Then you add the totals together. 
   So,1×2+2×7+3×6+4×5+5×4+6×3+7×2=106. 

2) If the first letter of the NRIC starts with T or G, add 4 to the total. 

3) Then you divide the number by 11 and get the remainder. 106/11=9r7 

4) You can get the alphabet depending on the IC type (the first letter 
   in the IC) using the code below: 
   If the IC starts with S or T: 
   0=J, 1=Z, 2=I, 3=H, 4=G, 5=F, 6=E, 7=D, 8=C, 9=B, 10=A 
   If the IC starts with F or G: 
   0=X, 1=W, 2=U, 3=T, 4=R, 5=Q, 6=P, 7=N, 8=M, 9=L, 10=K
"""
from re import match
code_ST = []
code_FG = []

def run_immediately(decorated):
    decorated()
    return decorated

@run_immediately
def populate_code_list():
	"""
    Populate the two lists above in value, letter format for the whole
    list of codes.
    """
	letter_code_ST = "JZIHGFEDCBA"
	letter_code_FG = "XWUTRQPNMLK"
	for pos in range(
	    len(letter_code_ST)):  #Interestingly, the values start from 0
		code_ST.append(pos)  # Number first
		code_ST.append(letter_code_ST[pos])
	for pos in range(len(letter_code_FG)):
		code_FG.append(pos)
		code_FG.append(letter_code_FG[pos])

def validate_NRIC(nric):
	"""Checks if NRIC is valid. Returns an error message if not."""
	if len(nric) != 9:  # invalid length
		return "Invalid length (must be exactly 9 characters, was given %d.)" % len(
		    nric)

	# Constants
	NRIC_ID = nric[0]
	LAST_LETTER = nric[-1]
	NUMBERS = nric[1:-1]

	if not match(r'[STFG]', nric):
		# First letter is not S, T, F or G
		return "Invalid NRIC ID: %s" % NRIC_ID

	# The NRIC first and last letters should be a letter, the middle should
	# be all numbers (7 numbers exactly)
	if match(r'[STFG][0-9]+[A-Z]', nric) is None:
		return "Invalid format: %s" % nric

	checksum = calculate_checksum(NRIC_ID, NUMBERS)
	last_letter_value = checksum % 11
	if last_letter_value == get_value(LAST_LETTER, NRIC_ID):
		return "Okay."
	else:
		return "Invalid NRIC, last letter must be %s." % get_letter(
		    last_letter_value, NRIC_ID)

def calculate_checksum(IC_type, numbers):
	"""Calculate checksum of NRIC."""
	checksum = 0
	# Check letter
	if IC_type == 'G' or IC_type == 'T':
		checksum += 4
	# Check first number
	first_num = int(numbers[0])
	checksum += first_num * 2
	# Remaining numbers
	multiplier = 7
	for num_str in numbers[
	    1:]:  # Get all the numbers except for the first one.
		num = int(num_str)
		checksum += num * multiplier
		multiplier -= 1
	return checksum

def get_value(letter, IC_type):
	"""
    Returns value of last letter of NRIC, if either `letter` or `IC_type` is
    invalid, returns None.
    """
	try:
		if IC_type == 'S' or IC_type == 'T':
			index_of_letter = code_ST.index(letter)
			return code_ST[index_of_letter -
			               1]  # Number is always before letter
		elif IC_type == 'F' or IC_type == 'G':
			index_of_letter = code_FG.index(letter)
			return code_FG[index_of_letter - 1]
		else:
			# IC_type is invalid
			return None
	except ValueError:
		# letter is invalid
		return None

def get_letter(value, IC_type):
	"""
    Get last letter of NRIC from value and IC_type. If any of the arguments
    are invalid, returns None.
    """
	if value > 10 or value < 0:
		# Invalid value (must be between 0 to 10)
		return None
	elif IC_type == 'S' or IC_type == 'T':
		index_of_value = code_ST.index(value)
		return code_ST[index_of_value + 1]  # Letter is always after number.
	elif IC_type == 'F' or IC_type == 'G':
		index_of_value = code_FG.index(value)
		return code_FG[index_of_value + 1]
	else:
		# IC_type is invalid
		return None

# Examples:
#  > validate_NRIC('T0601033J')
# => Okay.
#  > validate_NRIC('T0601035J')
# => Invalid NRIC, last letter must be G.
#  > validate_NRIC('F5651631W')
# => Okay.
#  > validate_NRIC('TY8638264')
# => Invalid format: TY8638264
#  > validate_NRIC('T762348I')
# => Invalid length (must be exactly 9 characters, was given 8.)
#  > validate_NRIC('A6726152F')
# => Invalid NRIC ID: A

@run_immediately
def run():
	"""Run the checker."""
	continue_checking = True
	# Main loop
	while continue_checking:
		input_nric = input("Enter an NRIC to check: ").strip().upper()
		print(validate_NRIC(input_nric))
		print()
		if input("Any other NRICs to check? (y/n)").strip().lower() == "n":
			print("Thank you.")
			continue_checking = False
		print()
