import random
import re

def IsPrime(n):
    # Check if a given number is prime.
    # Returns true if prime, false otherwise.
    if n > 1:
        for i in range(2, int(n / 2)):
            if n % i == 0:
                return False
        return True
    else:
        return False


def createCharTable():
    # Build the character table.
    # Returns a list.

    # The index of each element is also its number values
    charTable = []

    # First character is the empty character.
    charTable.append(' ')

    # Build the rest of the character table by incrementing the ASCII code of lower-case character 'a'
    # until we get all lower-case characters from the alphabet.
    for i in range(0, 26):
        charTable.append(chr(ord('a') + i))

    return charTable


def ConvertCharToNumber(ch, charTable):
    # Given a character, find it in the charTable and return its index
    ch_pos = charTable.index(ch)
    return ch_pos


def ConvertNumberToChar(nr, charTable):
    # Given a number % 27, convert it to a character from the charTable
    ch = charTable[nr]
    return ch


def gcd(a, b):
    # The gcd is computed through a series of repeated divisions.
    # The recursion stops when the remainder of the division is 0.
    if b == 0:
        return a
    return gcd(b, a % b)


def GenerateKey(lower_bound, upper_bound, k, l):
    # Generates 2 random distinct prime numbers in a given interval.
    # Returns tuple: (n, (p, q)) where n -> public key, (p, q) -> private key
    primeNumbers = []
    while len(primeNumbers) < 2:
        randNr = random.randint(lower_bound, upper_bound)
        # Check if the generated number is prime, if it modulo 4 is 3, for easier computation of square roots
        # and if it wasn't already found.
        if IsPrime(randNr) and randNr % 4 == 3 and randNr not in primeNumbers:
            primeNumbers.append(randNr)
    # Compute the value n which is also the public key
    public_key = primeNumbers[0] * primeNumbers[1]
    # Try again if the public key isn't bigger than 27^k and smaller than 27^l
    if public_key > pow(27, l) or public_key < pow(27, k):
        public_key, (primeNumbers[0], primeNumbers[1]) = GenerateKey(lower_bound, upper_bound, k, l)
    return public_key, (primeNumbers[0], primeNumbers[1])


def SplitMsg(msg, k):
    # Split the message in chunks of k size. Each chunk is a separate element in splitMsg list.
    # Returns a list.
    splitMsg = []
    i = 0

    msg = EvenMsg(msg, k)

    while i < len(msg):
        splitMsg.append(msg[i:i + k])
        i += k
    return splitMsg


def EvenMsg(msg, k):
    # If message is not divisible by k, add the necessary empty characters at the end.
    while len(msg) % k != 0:
        msg += ' '
    return msg


def computeSplitValues(splitMsg, charTable, l):
    # Compute the numeric value of each block using the character table
    # Returns a list of values, where value at position 0 is the value of the first block, etc.

    splitValues = []
    i = 0
    while i < len(splitMsg):
        pair = splitMsg[i]

        pair_value = 0
        maxL = l - 1
        for j in range(len(pair)):
            pair_value += ConvertCharToNumber(pair[j], charTable) * pow(27, maxL)
            maxL -= 1
        splitValues.append(pair_value)
        i += 1
    return splitValues


def Encrypt(msg, public_key, plaintext_block_size, ciphertext_block_size):
    # Create the character table
    charTable = createCharTable()

    # Add empty character if message length is not even
    evenMsg = EvenMsg(msg, plaintext_block_size)

    # Split the message into blocks of size plaintext_block_size
    splitMsg = SplitMsg(evenMsg, plaintext_block_size)

    # Compute the numeric value of each block
    splitValues = computeSplitValues(splitMsg, charTable, plaintext_block_size)

    cipher = []
    # Compute the cipher text
    for i in range(len(splitValues)):
        c = pow(splitValues[i], 2) % public_key
        cipher.append(c)

    # Transform the cipher from numeric to string
    cipherText = ""
    for i in range(len(cipher)):
        val = cipher[i]

        maxK = ciphertext_block_size - 1

        while maxK >= 0:
            quotient, remainder = divmod(val, pow(27, maxK))
            cipherText += ConvertNumberToChar(quotient % 27, charTable)
            maxK -= 1
            val = remainder

    return cipherText


# The extended euclidean algorithm
def extended_gcd(a, b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # In order: GCD and the Bezout coefficients
    return old_r, old_s, old_t

# Transform the cipher from numeric to string
def convert_numbers_to_text_chunk(d, plaintext_block_size, charTable):
    maxK = plaintext_block_size - 1
    val = d
    cipherText = ""

    while maxK >= 0:
        quotient, remainder = divmod(val, pow(27, maxK))
        cipherText += ConvertNumberToChar(quotient % 27, charTable)
        maxK -= 1
        val = remainder

    return cipherText


def Decrypt(msg, private_key, plaintext_block_size, ciphertext_block_size):
    # Create the character table
    charTable = createCharTable()

    # Add empty character if message length is not even
    evenMsg = EvenMsg(msg, ciphertext_block_size)

    # Split the message into blocks of size ciphertext_block_size
    splitMsg = SplitMsg(evenMsg, ciphertext_block_size)

    # Compute the numeric value of each block
    splitValues = computeSplitValues(splitMsg, charTable, ciphertext_block_size)

    plaintext_possibilities = []

    # private_key[0] is p and private_key[1] is q
    for i in range(len(splitValues)):
        c1mod = pow(splitValues[i], (private_key[0] + 1) // 4) % private_key[0]
        c2mod = pow(splitValues[i], (private_key[1] + 1) // 4) % private_key[1]
        _, y_p, y_q = extended_gcd(private_key[0], private_key[1])
        # Chinese remainder theorem
        d1 = (y_p * private_key[0] * c2mod + (y_q * private_key[1] * c1mod)) % (private_key[0] * private_key[1])
        d2 = (y_p * private_key[0] * (private_key[1] - c2mod) + (y_q * private_key[1] * c1mod)) % (private_key[0] * private_key[1])
        d3 = (y_p * private_key[0] * c2mod + (y_q * private_key[1] * (private_key[0] - c1mod))) % (private_key[0] * private_key[1])
        d4 = (y_p * private_key[0] * (private_key[1] - c2mod) + (y_q * private_key[1] * (private_key[0] - c1mod))) % (private_key[0] * private_key[1])

        d1convert = convert_numbers_to_text_chunk(d1, plaintext_block_size, charTable)
        d2convert = convert_numbers_to_text_chunk(d2, plaintext_block_size, charTable)
        d3convert = convert_numbers_to_text_chunk(d3, plaintext_block_size, charTable)
        d4convert = convert_numbers_to_text_chunk(d4, plaintext_block_size, charTable)

        plaintext_possibilities.append([d1convert, d2convert, d3convert, d4convert])

    return plaintext_possibilities

def ValidateText(text):
    # Checks if text contains only lower case letters and empty characters
    response = re.search("^[a-z ]+$", text)
    if response:
        return True
    return False

def RunAutomatedTests():
    # Run the encryption and decryption on a predefined set of data
    public_key, private_key = GenerateKey(1, 1000, 2, 3)
    messages = ["game", "madara uchiha", "light yagami", "darth vader"]

    for i in range(len(messages)):
        isCorrect = True
        print("Running for " + messages[i] + " --> ", end=' ')

        if not ValidateText(messages[i]):
            print("Plaintext validation failed.")
            continue

        cipherText = Encrypt(messages[i], public_key, 2, 3)

        if not ValidateText(cipherText):
            print("Ciphertext validation failed.")
            continue

        plainText = Decrypt(cipherText, private_key, 2, 3)
        splitMsg = SplitMsg(messages[i], 2)
        for j in range(len(splitMsg)):
            if splitMsg[j] not in plainText[j]:
                print("Original and decrypted do not match at " + str(j))
                print(splitMsg[j])
                print(plainText[j])
                isCorrect = False

        if isCorrect:
            print("All good")
            print("Ciphertext: " + cipherText)
            print("Plaintext possibilities: ", end=' ')
            print(plainText)
        print("------------")

def main():
    public_key, private_key = GenerateKey(1, 1000, 2, 3)
    while True:
        RunAutomatedTests()
        msg = input("Message to encrypt: ")
        if ValidateText(msg):
            print(Encrypt(msg, public_key, 2, 3))
        else:
            print("Plaintext validation failed.")

        msg = input("Message to decrypt: ")

        if ValidateText(msg):
            print(Decrypt(msg, private_key, 2, 3))
        else:
            print("Plaintext validation failed.")



main()
