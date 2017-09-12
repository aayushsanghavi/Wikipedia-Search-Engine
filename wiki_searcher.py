from include import *
import operator
import time

print "Please wait while the files are being loaded"
title_tags = open("files/title_tags.txt", "r")
title_position = pickle.load(open("files/title_positions.pickle", "rb"))
word_position = pickle.load(open("files/word_positions.pickle", "rb"))
field_map = {"t" : 0, "b" : 1, "i" : 2, "c" : 3}

files = []
for f in field_chars :
	file = "files/" + f + ".txt"
	fp = open(file, "r")
	files.append(fp)

while True :
	results = []
	documents = {}
	query_words = []
	query = raw_input("> ")
	query = query.lower().strip()
	start = time.time()
	if (query == "exit") :
		break

	if ":" in query :
		query_bag = query.split(",")
		for q in query_bag :
			field, query = q.split(":")
			query_words = query.split()
			for word in query_words :
				word = stemmer.stemWord(word)
				if word in word_position and field in word_position[word] :
					position = word_position[word][field]
					files[field_map[field]].seek(position)
					s = files[field_map[field]].readline()[: -1]
					if "," in s :
						docs = s.split(",")
						for doc in docs :
							document, score = doc.split(":")
							if document not in documents :
								documents[document] = 0.0
							documents[document] += float(score)
					else :
						document, score = s.split(":")
						if document not in documents :
							documents[document] = 0.0
						documents[document] += float(score)
	else :
		query_bag = query.split()
		length = len(query_bag)
		for i in range(length) :
			query_bag[i] = stemmer.stemWord(query_bag[i])

		for word in query_bag :
			if word not in stop_words and word in word_position:
				query_words.append(word)

		for word in query_words :
			positions = word_position[word]
			for field in positions :
				position = positions[field]
				files[field_map[field]].seek(position)
				s = files[field_map[field]].readline()[: -1]
				if "," in s :
					docs = s.split(",")
					for doc in docs :
						document, score = doc.split(":")
						if document not in documents :
							documents[document] = 0.0
						documents[document] += float(score)
				else :
					document, score = s.split(":")
					if document not in documents :
						documents[document] = 0.0
					documents[document] += float(score)

	documents = sorted(documents.items(), key = operator.itemgetter(1), reverse = True)
	number_of_results = 0
	for document in documents :
		if number_of_results == 10 :
			break

		position = title_position[int(document[0]) - 1]
		title_tags.seek(position)
		title = title_tags.readline()[: -1]
		results.append(title)
		number_of_results += 1

	end = time.time()
	if len(results) == 0 :
		print "No reults found"
		print "Time taken - " + str(end - start) + "s"
	else :
		print "Results retrieved in - " + str(end - start) + "s"

	for result in results :
		print result