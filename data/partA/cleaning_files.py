
import collections
import os
import re
import fileinput


pos='pos2.txt'
neg='neg2.txt'

def stop_words():
	with open('stopwords.txt','r') as f:
		stopwords=[line.strip() for line in f]
		print stopwords
	return stopwords

def remove_stopwords(fname):
	inputfile=open(fname,"r")
	outfile=open('temp.txt','w+')

	data=[line.lower() for line in inputfile]
	outfile.writelines(data)
	outfile.seek(0,0)

	cleanedfile=open('cleaned'+fname,'w+')
	stopwords=stop_words()

	for line in outfile:
		for word in stopwords:
			line= re.sub(r'([^A-Za-z]|^)'+word+r'([^A-Za-z]|$)',' ',line)

		cleanedfile.write(line)

	outfile.close()
	
	lines=[]

	cleanedfile.seek(0,0)
	for line in cleanedfile:
		line = re.sub(r"[^A-Za-z\']"," ", line)
		line = re.sub(r'(^' ')' ,"", line)
		line = re.sub(r"[\']", "", line)
		line = re.sub(r"(^\s+)",'',line)
		lines.append(line+'\n')

	cleanedfile.seek(0,0)
	for line in lines:
		cleanedfile.write(line)

	cleanedfile.close()
	outfile.close()
	os.remove('temp.txt')

# remove_blanklines(pos)
