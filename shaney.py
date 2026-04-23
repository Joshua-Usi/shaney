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
		wordfreq = contexts.get(key, {})
		wordfreq[word] = wordfreq.get(word, 0) + 1
		contexts[key] = wordfreq
		# print(key, word, wordfreq[word])
		context = context[1:] + [word]
		
# Generate semi-random output.
# Print a random starting point and continue from there.
# 'starters' is a list of possible starter contexts.
def generate(f, starters, contexts):
	context = random.choice(starters)
	f.write(" ".join(context))
	while True:
		key = tuple(context)
		wordfreq = contexts.get(key, {})
		if not wordfreq:
				break
		word = choose(wordfreq)
		f.write(" " + word)
		context = context[1:] + [word]
	f.write("\n")

# Randomly choose one word from a {word->frequency}
# dictionary, the choice being weighted by frequency.
def choose(wordfreq):
	# Calculate the total instances.
	total = 0
	for w,count in wordfreq.items():
			total += count
	# Choose a random instance.
	chosen = random.randint(1,total)
	# Walk through to find it.
	sofar = 0
	for word,count in wordfreq.items():
		sofar += count
		if chosen <= sofar:
			return word
	assert(0)

# Generate a semi-random sequence of words that
# mimic the probabilities of the input text.
def main():
	# Initialise.

	parser = argparse.ArgumentParser()
	parser.add_argument("--data", type=str, default="data/")
	parser.add_argument("--n", type=int, default="2")

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

