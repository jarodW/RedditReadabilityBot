import nltk
from nltk.tokenize import RegexpTokenizer

def normalizeWord(word):
	return word.strip().lower()

def isVowel(char):
		if(char == 'a' or char == 'e' or char =='i' or char == 'o' or char =='u' or char == 'y'):
			return 1
		return 0

def getCharacters(words):
    characters = 0
    for word in words:
        characters += len(word)
    return characters		
		
def countSyllablesInWord(word):
	word = normalizeWord(word)
	if not word:
		return 0
	counter = 0
	for i in range(len(word)):
		if word[i] == 'e' and i == len(word) - 1:
			continue
		elif i > 0 and isVowel(word[i]) and isVowel(word[i-1]):
			continue
		elif(isVowel(word[i])):
			counter += 1
			
	if counter == 0:
		counter = 1
	return counter

def getSyllables(words):
		count = 0
		for word in words:
			count += countSyllablesInWord(word)
		return count
	
def getWords(text):
	tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+[^)]$')
	special_chars = ['.', ',', '!', '?','(',')']
	words = []
	words = tokenizer.tokenize(text)
	realWords = []
	for word in words:
		if word in special_chars or word == " ":
			pass
		else:
			new_word = word.replace(",","").replace(".","")
			new_word = new_word.replace("!","").replace("?","")
			realWords.append(new_word)
	return realWords	

def getSentences(text):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(text)
	return sentences	

def fleschKincaid(text, words, syllables,sentences):
	return 205.835 - (84.6 * ( syllables / words)) - (1.015 * ( words / sentences))

def fleschKincaidGrade(text, words, syllables,sentences):
	c0 = -15.59
	c1 = .39
	c2 = 11.8
	return c0 + c1*(words/sentences)+c2*(syllables/words)

def automatedReadabilityIndex(chars, words, sentences):
    c0 = 4.71
    c1 = 0.5
    c2 = 21.43
    return c0 * (chars/ words) + c1 * (words / sentences) - c2
	
def computeIndex(text):
		sentences = float(len(getSentences(text)))
		words = getWords(text)
		numWords = float(len(words))
		syllables = float(getSyllables(words))
		chars = float(getCharacters(words))
		fk = fleschKincaid(text,numWords,syllables,sentences)
		fkg = fleschKincaidGrade(text, numWords, syllables,sentences)
		ari = automatedReadabilityIndex(chars, numWords, sentences)
		#formatting for reddit
		return "[Flesch Kincaid:](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)" + str(fk) + "\n\n[Flesch Kincaid Grade:](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch.E2.80.93Kincaid_grade_level)" + str(fkg) + "\n\n[ARI:](https://en.wikipedia.org/wiki/Automated_readability_index)" + str(ari)
