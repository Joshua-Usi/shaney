# !/usr/bin/python 
import os, sys, string, random

import argparse

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

	parser = argparse.ArgumentParser()
	parser.add_argument("--data", type=str, default="data/")
	parser.add_argument("--n", type=int, default=2)

	args = parser.parse_args()

	data_dir = args.data
	n = args.n

	if data_dir[-1] != "/":
		data_dir = data_dir + "/"

	# Build the frequency table by reading the input text(s).
	contexts = {}
	starters = []

	for filename in sorted(os.listdir(data_dir)):
		print("Reading " + data_dir + filename)
		words = open(data_dir + filename, encoding='utf-8').read().split()
		starters.append(words[:n])
		build(contexts, words, n)

	# Print words at random, starting at some initial context.
	out_file = "output.txt"
	print("Writing " + out_file)
	f = open(out_file, "w")
	generate(f, starters, contexts)
	f.close()

if __name__ == '__main__':
	main()
