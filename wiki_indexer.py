import operator
from math import *
from heapq import *
from include import *
from collections import *
import xml.etree.cElementTree as et

reload(sys)
sys.setdefaultencoding('utf-8')
title_index = defaultdict(list)
text_index = defaultdict(list)
category_index = defaultdict(list)
infobox_index = defaultdict(list)
output_files = []
title_position = []
word_position = {}

file_count = 0
page_count = 0
pages_per_file = 2000
arguments = sys.argv

xmlFile = arguments[1]
context = et.iterparse(xmlFile, events=("start", "end"))
context = iter(context)
title_tags = open("files/title_tags.txt", "w")

for event, elem in context :
	tag =  re.sub(r"{.*}", "", elem.tag)

	if event == "start" :
		if tag == "page" :
			page_count += 1
			title_tag_words = {}
			text_tag_words = {}
			category_words = {}
			infobox_words = {}

	if event == "end" :
		if tag == "text" :
			text = elem.text
			try :
				tempword = re.findall("\[\[Category:(.*?)\]\]", text)
				if tempword :
					for temp in tempword :
						temp = re.split(pattern, temp)
						for t in temp :
							t = t.lower()
							t = stemmer.stemWord(t)
							if t :
								if  t not in stop_words :
									if t not in category_words:
										category_words[t] = 0
									category_words[t] += 1	

				tempword = re.findall("{{Infobox(.*?)}}", text)
				if tempword :
					for temp in tempword :
						temp = re.split(pattern, temp)
						for t in temp :
							t = t.lower()
							t = stemmer.stemWord(t)
							if t :
								if  t not in stop_words :
									if t not in infobox_words :
										infobox_words[t] = 0
									infobox_words[t] += 1
			except :
				pass

			try :
				text = text.encode("utf-8")
				text = text.lower()
				text = re.split(pattern, text)
				total_words_per_page = 0

				for word in text :
					if word :
						if word not in stop_words :
							word = stemmer.stemWord(word)
							if word not in text_tag_words :
								text_tag_words[word] = 0
							text_tag_words[word] += 1

			except :
				pass

		if tag == "title" :
			text = elem.text

			try :
				text = text.encode("utf-8")
				title_string = text + "\n"
				text = text.lower()
				title_position.append(title_tags.tell())
				title_tags.write(title_string)
				text = re.split(pattern, text)

				for word in text :
					if word :
						if word not in stop_words :
							word = stemmer.stemWord(word)
							if word not in title_tag_words :
								title_tag_words[word] = 0
							title_tag_words[word] += 1

			except :
				pass

		if tag == "page" :
			index = "d"+str(page_count)
			for word in text_tag_words :
				s = index + ":" + str(text_tag_words[word])
				text_index[word].append(s)

			for word in title_tag_words :
				s = index + ":" + str(title_tag_words[word])
				title_index[word].append(s)

			for word in category_words :
				s = index + ":" + str(category_words[word])
				category_index[word].append(s)

			for word in infobox_words :
				s = index + ":" + str(infobox_words[word])
				infobox_index[word].append(s)

			if page_count % pages_per_file == 0 :
				file = "files/" + "t" + str(file_count) + ".txt"
				outfile = open(file, "w")
				for word in sorted(title_index) :
					index = ",".join(title_index[word])
					index = word + "-" + index+"\n"
					outfile.write(index)
				outfile.close()

				file = "files/" + "b" + str(file_count) + ".txt"
				outfile = open(file, "w")
				for word in sorted(text_index) :
					index = ",".join(text_index[word])
					index = word + "-" + index+"\n"
					outfile.write(index)
				outfile.close()

				file = "files/" + "c" + str(file_count) + ".txt"
				outfile = open(file, "w")
				for word in sorted(category_index) :
					index = ",".join(category_index[word])
					index = word + "-" + index+"\n"
					outfile.write(index)
				outfile.close()

				file = "files/" + "i" + str(file_count) + ".txt"
				outfile = open(file, "w")
				for word in sorted(infobox_index) :
					index = ",".join(infobox_index[word])
					index = word + "-" + index+"\n"
					outfile.write(index)
				outfile.close()

				outfile.close()
				file_count += 1
				title_index.clear()
				text_index.clear()
				category_index.clear()
				infobox_index.clear()

		elem.clear()

title_tags.close()
file = open("files/title_positions.pickle", "wb")
pickle.dump(title_position, file)
file.close()

file = "files/" + "t" + str(file_count) + ".txt"
outfile = open(file, "w")
for word in sorted(title_index) :
	index = ",".join(title_index[word])
	index = word + "-" + index+"\n"
	outfile.write(index)
outfile.close()

file = "files/" + "b" + str(file_count) + ".txt"
outfile = open(file, "w")
for word in sorted(text_index) :
	index = ",".join(text_index[word])
	index = word + "-" + index+"\n"
	outfile.write(index)
outfile.close()

file = "files/" + "c" + str(file_count) + ".txt"
outfile = open(file, "w")
for word in sorted(category_index) :
	index = ",".join(category_index[word])
	index = word + "-" + index+"\n"
	outfile.write(index)
outfile.close()

file = "files/" + "i" + str(file_count) + ".txt"
outfile = open(file, "w")
for word in sorted(infobox_index) :
	index = ",".join(infobox_index[word])
	index = word + "-" + index+"\n"
	outfile.write(index)
outfile.close()

file_count += 1
for f in field_chars :
	heap = []
	input_files = []
	file = "files/" + f + ".txt"
	fp = open(file, "w")
	output_files.append(fp)
	outfile_index = len(output_files) - 1

	for i in range(file_count) :
		file = "files/" + f + str(i) + ".txt"
		if not os.stat(file).st_size == 0 :
			fp = open(file, "r")
			input_files.append(fp)
		else :
			try :
				del input_files[i]
				os.remove(file)
			except :
				pass

	if len(input_files) == 0 :
		break

	for i in range(file_count) :
		try :
			s = input_files[i].readline()[:-1]
			heap.append((s, i))
		except :
			pass

	heapify(heap)
	i = 0
	try :
		while i < file_count :
			s, index = heappop(heap)
			word = s[: s.find("-")]
			posting_list = s[s.find("-") + 1 :]

			next_line = input_files[index].readline()[: -1]
			if next_line :
				heappush(heap, (next_line, index))
			else :
				i += 1

			if i == file_count :
				break

			while True :
				try :
					next_s, next_index = heappop(heap)
				except IndexError :
					break

				next_word = next_s[: next_s.find("-")]
				next_posting_list = next_s[next_s.find("-") + 1 :]
				if next_word == word :
					posting_list = posting_list + "," + next_posting_list
					next_new_line = input_files[next_index].readline()
					if next_new_line :
						heappush(heap, (next_new_line, next_index))
					else :
						i += 1
				else :
					heappush(heap, (next_s, next_index))
					break

			if word not in word_position :
				word_position[word] = {}
			word_position[word][f] = output_files[outfile_index].tell()
			postings = posting_list.split(",")
			documents = {}
			idf = log10(page_count / len(postings))
			for posting in postings :
				d = posting[posting.find("d") + 1 : posting.find(":")]
				freq = posting[posting.find(":") + 1 :]
				freq = int(freq)
				tf = 1 + log10(freq)
				documents[str(d)] = round(idf * tf, 2)

			documents = sorted(documents.items(), key = operator.itemgetter(1), reverse = True)
			number_of_results = 0
			score = ""
			for document in documents :
				if number_of_results == 10 :
					break
				score = score + document[0] + ":" + str(document[1]) + ","
				number_of_results += 1

			score = score[:-1] + "\n"
			output_files[outfile_index].write(score)

	except IndexError :
		pass

	output_files[outfile_index].close()

	try :
		for i in range(file_count) :
			file = "files/" + f + str(i) + ".txt"
			input_files[i].close()
			os.remove(file)
	except :
		pass

file = open("files/word_positions.pickle", "wb")
pickle.dump(word_position, file)
file.close()
