import math
import pickle
import buildvoc

pos='pos2.txt'
neg='neg2.txt'
positive,negative={},{}

def settingdicts():
	global positive,negative
	poslist=buildvoc.createlist('train_'+pos)
	posdict=buildvoc.createdict(poslist)
	buildvoc.pickleout(posdict,'pos_dict')
	positive=buildvoc.pickleIn('pos_dict')
	outfile=open('positive.txt','w+')
	for line in positive:
		outfile.write(line)
	outfile.close()

	neglist=buildvoc.createlist('train_'+neg)
	negdict=buildvoc.createdict(neglist)
	buildvoc.pickleout(negdict,'neg_dict')
	negative=buildvoc.pickleIn('neg_dict')
	outfile=open('negative.txt','w+')
	for line in negative:
		outfile.write(line)
	outfile.close()

def noofreviews(fname):
	number_of_reviews = 0
	with open(fname) as datafile:
		for line in datafile:
			if line.strip():
				number_of_reviews += 1
        	
	return number_of_reviews


def totalwordsinclass(classname):
	global negative,positive
	count=0
	if classname=='+':
		dt=positive
	else:
		dt=negative

 	for word in dt:
 		count+=dt[word]
	return count	

def prior(classname):
	totalpos= noofreviews('train_'+pos)
	totalneg= noofreviews('train_'+neg)
	totalreviews=totalpos+totalneg

	if classname=='+':
		return math.log((float)(totalpos)/totalreviews,2)
	else :
		return math.log((float)(totalneg)/totalreviews,2)

def wordcount(word,classname):
	global negative,positive

	if classname=='+':
		dt=positive
	else:
		dt=negative

	if word in dt :
		return dt[word]
	else:
		return 0
	
def classconditional(word,classname):
	vocsize=noofreviews('vocabulary.txt')
	classfreq=totalwordsinclass(classname)
	count=wordcount(word,classname)
	cond_prob = float(count + 1)/(classfreq+vocsize)
	return cond_prob

def create_model():
    global negative,positive,prob
    #here i made mistake bakayaro
    prob={}
    vocab=open('vocabulary.txt','r')
    for word in vocab:
    	word=word.strip('\n')
    	# print word
    	posprob=math.log(classconditional(word,'+'),2)
    	negprob=math.log(classconditional(word,'-'),2)
    	prob[word]=[posprob,negprob]
    buildvoc.pickleout(prob,'classifier')
    MNB=buildvoc.pickleIn('classifier')
    outfile=open('classifier.txt','w+')
    for line in MNB:
    	outfile.write(line)
    outfile.close()
print wordcount('separate','+')