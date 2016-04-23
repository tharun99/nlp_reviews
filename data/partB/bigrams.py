import re
from collections import Counter
import pickle
import os
import math
import sys

pos='pos2.txt'
neg='neg2.txt'


def stop_words():
    with open('stopwords.txt','r') as f:
        stopwords=[line.strip() for line in f]
        # print stopwords
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
        line = re.sub(r"(^)","* ",line)
        line = re.sub(r"($)",' #',line)
        # line = re.sub(r"[\"|\...",'',line)
        # line = re.sub(r"[\s|^][a-z][\s|$]"," ",line)
        # line = re.sub(r"[\s|\.|\"]"," ",line)
        lines.append(line+'\n')

    cleanedfile.seek(0,0)
    for line in lines:
        cleanedfile.write(line)

    cleanedfile.close()
    outfile.close()
    os.remove('temp.txt')

def pickleout(temp,fname):
    pickle_out = open(fname+'.p', 'wb')
    pickle.dump(temp, pickle_out)
    pickle_out.close()

def pickleIn(fname):
    pickle_in = open(fname+'.p','rb')
    db1 = pickle.load(pickle_in)  
    return db1


def createunigramslist(fname):
    inputfile=open(fname,'r')
    filecontents=inputfile.read()
    inputfile.close()
    words_list=filecontents.split()
    s=[]
    for word in words_list:
        s.append(word)

    return s

def createunigramdict(word_list):
    worddict = Counter(word_list)
    worddict = {i:worddict[i] for i in worddict if worddict[i]>=2 and len(i)>2}
    return worddict

def noofreviews(fname):
    number_of_reviews = 0
    with open(fname) as datafile:
        for line in datafile:
            if line.strip():
                number_of_reviews += 1
            
    return number_of_reviews

def bigramcount(word,classname):
    global bipositive,binegative
    if classname=='+':
        dt=bipositive
    else:
        dt=binegative

    if word in dt :
        return dt[word]
    else:
        return 0


def unigramcount(word,classname):
    global uninegative,unipositive

    if classname=='+':
        dt=unipositive
    else:
        dt=uninegative

    if word in dt :
        return dt[word]
    else:
        return 0

def totalwordsinclass(classname):
    global uninegative,unipositive
    count=0
    if classname=='+':
        dt=unipositive
    else:
        dt=uninegative

    for word in dt:
        count+=dt[word]
    return count    

def prior(classname):
    totalpos= noofreviews('train_'+pos)
    totalneg= noofreviews('train_'+neg)
    totalreviews=totalpos+totalneg

    if classname=='+':
        return math.log10((float)(totalpos)/totalreviews)
    else :
        return math.log10((float)(totalneg)/totalreviews)

# def total(classname):
#     if classname=='+':
        

def classconditional(w1,w2,classname):
    voc_size=noofreviews('bivocabulary.txt')+noofreviews('univocabulary.txt')
    bigram=(w1,w2)
    num=bigramcount(bigram,classname)
    den=unigramcount(w1,classname)

    if num!=0:
        cond_prob=math.log10(float(num+1)/(den+voc_size))
    else:
        voc_size=noofreviews('univocabulary.txt')
        num=den
        den=totalwordsinclass(classname)
        cond_prob1=float(num+1)/(den+voc_size)
        num=unigramcount(w2,classname)
        cond_prob2=float(num+1)/(den+voc_size)
        cond_prob=math.log10(cond_prob1)+math.log10(cond_prob2)

    return (cond_prob)

def findclasscond(line,classname):
    words=line.split()
    logprob=0

    for i in range(len(words)-1):
        logprob+=classconditional(words[i],words[i+1],classname)

    return logprob


def findposterior(line,classname):
    return findclasscond(line,classname)+prior(classname)


def tenfold(doc,num):
    infile=open('cleaned'+doc)
    for i in range(1,11):
        outfile=open(str(i)+doc,'w')
        for j in range(40):
            # print str(j)+'\n'
            outfile.write(infile.readline())
        outfile.close()

def destroy(fname):
    if os.path.exists(fname):
        os.remove(fname)

def createbigramlist(fname):
    inputfile=open(fname,'r')
    content=inputfile.read()
    words=content.split()    
    bigrams=zip(words,words[1:])
    s=[]
    for word in bigrams:
        s.append(word)
    return s

def createbigramdict(bigramlist):
    bigramdict = Counter(bigramlist)
    bigramdict = {i:bigramdict[i] for i in bigramdict if bigramdict[i]>=2}
    # print bigramdict
    return bigramdict


def clear_all():
    for doc in [pos,neg]:
        for typ  in ['train_']:
            destroy(typ+doc)
    destroy('vocabulary.txt')
    for doc in ['pos_','neg_','vocab_']:
        destroy(doc+'dict.p')

def crossvalidate():
    global uninegative,unipositive,bipositive,binegative
    accuracysum=0
    itr=0
    for i in range(1,11):   
        # print str(i)+'\n'
        unipositive,uninegative,bipositive,binegative={},{},{},{}

        posfreq=0
        negfreq=0
        voc_size=0

        postrain,negtrain='',''

        for j in range(1,11):
            
            if j!=i:
                # print str(j)+'='+'\n'
                inpos=open(str(j)+pos)
                postrain+=inpos.read()
                inpos.close()

                inneg=open(str(j)+neg)
                negtrain+=inneg.read()
                inneg.close()

        
        intrain=open('train_'+pos,'w')
        intrain.write(postrain)
        intrain.close()

        intrain=open('train_'+neg,'w')
        intrain.write(negtrain)
        intrain.close()

        trainset=(postrain+negtrain).split("\n")

        uniposlist=createunigramslist('train_'+pos)
        uniposdict=createunigramdict(uniposlist)
        pickleout(uniposdict,'unipos_dict')
        unipositive=pickleIn('unipos_dict')


        # outfile=open('positive.txt','w+')
        # for word in positive:
        #     outfile.write(word+':'+str(positive[word])+'\n')
        # outfile.close()
        unineglist=createunigramslist('train_'+neg)
        uninegdict=createunigramdict(unineglist)
        pickleout(uninegdict,'unineg_dict')
        uninegative=pickleIn('unineg_dict')

        # outfile=open('negative.txt','w+')
        # for i in negative:
        #   outfile.write(i+str(negative[i])+'\n')
        # outfile.close()
        biposlist=createbigramlist('train_'+pos)
        biposdict=createbigramdict(biposlist)
        pickleout(biposdict,'bipos_dict')
        bipositive=pickleIn('bipos_dict')

        bineglist=createbigramlist('train_'+neg)
        binegdict=createbigramdict(bineglist)
        pickleout(binegdict,'bineg_dict')
        binegative=pickleIn('bineg_dict')

        totalunilist=uniposlist+unineglist
        univocab=createunigramdict(totalunilist)
        pickleout(univocab,'univocabdict')
        univocablry=pickleIn('univocabdict')
        # print univocablry

        totalbilist=biposlist+bineglist
        bivocab=createbigramdict(totalbilist)
        pickleout(bivocab,'bivocabdict')
        bivocablry=pickleIn('bivocabdict')
        # print bivocablry
        
        outfile=open('univocabulary.txt','w+')
        for word in univocablry:
            outfile.write(word+'\n')
        outfile.close()

        outfile=open('bivocabulary.txt','w+')       
        for word in bivocablry:
            outfile.write(str(word)+'\n')
            
        outfile.close()

        # create_model()
        # prob=pickleIn('classifier')

        fpos,fneg,tpos,tneg=0,0,0,0

        possample=open(str(i)+pos,'r')
        content=possample.readlines()

        # print wordcount('very','+')
        # print classconditional('very','+')

        for line in content:
            sys.stdout.write('*')
            sys.stdout.flush()
            postpos=findposterior(line,'+')
            postneg=findposterior(line,'-')
            if postpos>postneg:
                tpos +=1
            else:
                fneg +=1

        negsample=open(str(i)+neg,'r')
        content=negsample.readlines()

        for line in content:
            postpos=findposterior(line,'+')
            postneg=findposterior(line,'-')
        #print possample
            if postpos<postneg:
                tneg +=1
            else:
                fpos +=1

        print fpos,fneg,tneg,tpos

        accuracy=(tpos+tneg)/float(tpos+tneg+fpos+fneg)
        itr+=1
        print 'accuracy'+str(itr)+'=',accuracy
        precision= (tpos)/float(tpos+fpos)
        print 'precision'+str(itr)+'=',precision
        recall= (tpos)/float(tpos+fneg)

        accuracysum+=accuracy
        clear_all()
    avg_accuracy=accuracysum/10.0
    print avg_accuracy

def main():
    remove_stopwords(pos)
    remove_stopwords(neg)
    postotal=noofreviews('cleaned'+pos)
    negtotal=noofreviews('cleaned'+neg)
    # createbigrams('cleaned'+pos)
    tenfold(pos,postotal)
    tenfold(neg,negtotal)
    crossvalidate()

main()