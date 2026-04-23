# !/usr/bin/python 
import os, sys, string, random

# Markov chain word generator.

# Map each context to {word->frequency}.
# 'contexts' is a frequency table, populated here.
# 'words' is an ordered list of words.
# 'n' is the number of words in each context window.
def build(contexts, words, n):
	context = words[:n]
	for word in words[n:]:
		key = tuple(context)
		word_freq = contexts.get(key, {})
		word_freq[word] = word_freq.get(word, 0) + 1
		contexts[key] = word_freq
		# print(key, word, word_freq[word])
		context = context[1:] + [word]
		
# Generate semi-random output.
# Print a random starting point and continue from there.
# 'starters' is a list of possible starter contexts.
def generate(f, starters, contexts):
	context = random.choice(starters)
	f.write(" ".join(context))
	while True:
		key = tuple(context)
		word_freq = contexts.get(key, {})
		if not word_freq:
				break
		word = choose(word_freq)
		f.write(" " + word)
		context = context[1:] + [word]
	f.write("\n")

# Randomly choose one word from a {word->frequency}
# dictionary, the choice being weighted by frequency.
def choose(word_freq):
	# Calculate the total instances.
	total = 0
	for w,count in word_freq.items():
			total += count
	# Choose a random instance.
	chosen = random.randint(1,total)
	# Walk through to find it.
	so_far = 0
	for word,count in word_freq.items():
		so_far += count
		if chosen <= so_far:
			return word
	assert(0)

# Generate a semi-random sequence of words that
# mimic the probabilities of the input text.
def main():
	# Initialise.
	data_dir = "data/"
	n = 2
	for arg in sys.argv[1:]:
		if arg.isnumeric(): n = int(arg)
		else: data_dir = arg

	# Build the frequency table by reading the input text(s).
	contexts = {}
	starters = []

	for filename in sorted(os.listdir(data_dir)):
		print("Reading " + data_dir + filename)
		words = open(data_dir + filename, encoding='utf-8').read().split()
		starters.append(words[:2])
		build(contexts, words, 2)

	# Print words at random, starting at some initial context.
	out_file = "output.txt"
	print("Writing " + out_file)
	f = open(out_file, "w")
	generate(f, starters, contexts)
	f.close()

if __name__ == '__main__':
	main()
