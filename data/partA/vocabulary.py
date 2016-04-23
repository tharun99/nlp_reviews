import re
from collections import Counter
import pickle

pos='pos2.txt'
neg='neg2.txt'


def pickleout(temp,fname):
    pickle_out = open(fname+'.p', 'wb')
    pickle.dump(temp, pickle_out)
    pickle_out.close()

def pickleIn(fname):
    pickle_in = open(fname+'.p','rb')
    db1 = pickle.load(pickle_in)    
    return db1

def createlist(fname):
	inputfile=open(fname,'r')
	filecontents=inputfile.read()
	inputfile.close()
	words_list=filecontents.split()
	s=[]
	for word in words_list:
		s.append(word)

	return s


def createdict(word_list):
	worddict = Counter(word_list)
	worddict = {i:worddict[i] for i in worddict if worddict[i]>=2}
	return worddict

def createvocab():
	poslist=createlist('train_'+pos)
	neglist=createlist('train_'+neg)
	totallist=poslist+neglist
	vocab=createdict(totallist)
	pickleout(vocab,'vocabdict')
	vocablry=pickleIn('vocabdict')
	outfile=open('vocabulary.txt','w+')

	for i in vocablry:
		outfile.write(i+'\n')

	outfile.close()