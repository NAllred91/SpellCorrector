import sys
from operator import itemgetter
import time

dictionary = open(sys.argv[1], 'r')
word = sys.argv[2]
vowel = ["a", "e", "i","o", "u"]
results = {}
worstRating = 1000
# An implementation of levenshtein distance
def levenshteinDistance(word1,word2):
    if len(word1) > len(word2):
        temp = word1
        word1 = word2
        word2 = temp
    current = range(len(word1) + 1)
    for index2,char2 in enumerate(word2):
        new = [index2+1]
        for index1,char1 in enumerate(word1):
            if char1 == char2:
                new.append(current[index1])
            else:
                new.append(1 + min((current[index1], current[index1 + 1], new[-1])))
        current = new

        
    return current[-1]	

# Return a word without vowels
def vowelRemoval(word):
	result = []

	for letter in word:
		if letter not in vowel:
			result.append(letter)

	return "".join(result)

# Return a vowel/consonant representation of a word
def simplify(word):
	result = []

	for letter in word:
		if letter in vowel:
			result.append('x')
		else:
			result.append('o')

	return "".join(result)

# Return a word with consecutive duplicates combined
def combineDuplicates(word):
	result = []
	resultPosition = 0
	letters = list(word)

	for x in range(0, len(letters)):
		
		if(x < len(letters) - 1 and letters[x] != letters[x + 1]):
			result.append(letters[x])
		if(x == len(letters) - 2):
			result.append(letters[x+1])
	
	return "".join(result)


# Return a rating for the line
# Once a word is obviously failing, we just return
# 1000 in order to avoid extra computations
def wordRating(word,line):

	bonusPoints = 0

	if(abs(len(word) - len(line)) > len(word) / 2 or abs(len(word) - len(line)) > len(line) / 2):
		return 1000


	sansVowelRating = levenshteinDistance(vowelRemoval(word), vowelRemoval(line))

	if(sansVowelRating < len(word) / 2 or sansVowelRating < 4):
		sansDuplicateRating = levenshteinDistance(combineDuplicates(word), combineDuplicates(line))
	else:
		return 1000

	if(sansVowelRating + sansDuplicateRating < 2 * worstRating):
		simplifiedRating = levenshteinDistance(simplify(word), simplify(line))
	else:
		return 1000

	if(sansVowelRating + sansDuplicateRating + simplifiedRating < 2 * worstRating):
		withVowelRating = levenshteinDistance(word,line)
	else:
		return 1000

	# Some bonus points for further pinpointing the correct word!
	if(combineDuplicates(vowelRemoval(word)) == combineDuplicates(vowelRemoval(line))):
		bonusPoints += abs(
		(len(line) - len(combineDuplicates(vowelRemoval(line)))) 
		- (len(word) - len(combineDuplicates(vowelRemoval(word)))))

	if(sansDuplicateRating == 0):
		bonusPoints += 2 * abs(
		(len(line) - len(combineDuplicates(line))) 
		- (len(word) - len(combineDuplicates(word))))

	if(sansVowelRating == 0):
		bonusPoints += 2 * abs(
		(len(line) - len(vowelRemoval(line))) 
		- (len(word) - len(vowelRemoval(word))))

	intersect = [val for val in list(word) if val in list(line)]

	bonusPoints += (len(intersect) - (len(list(word)) - len(intersect))) / 2.5

	bonusPoints += (len(intersect) - (len(list(line)) - len(intersect))) / 2.5

	if(list(line)[0] == list(word)[0]):
		bonusPoints += 1
	
	if(word == line):
		bonusPoints += len(word)

	return withVowelRating + sansVowelRating + simplifiedRating + sansDuplicateRating - bonusPoints
	
		

# Grab the start time
start = time.time()

# Get the first line to set the "worstWord" and "worstRating"
worstWord = dictionary.readline().strip()
worstRating = wordRating(word, worstWord)
results[worstWord] = worstRating

# Iterate through the dictionary and get the rating of each word
for line in dictionary:
	lineWord = line.strip()
	rating = wordRating(word, lineWord)

	if(len(results) < 10):
		results[lineWord] = rating

		if(worstRating < rating):
			worstRating = rating
			worstWord = lineWord

	elif(rating < worstRating):
		del results[worstWord]
		results[lineWord] = rating
		worstWord = max(results, key=results.get)
		worstRating = results[worstWord]

finalResults = sorted(results.items(), key=itemgetter(1))
end = time.time()

print ""
for word in finalResults:
	print word[0]

print("Total Time: " + str(end - start) + " seconds\n")





 

 