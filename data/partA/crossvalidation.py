import re
from collections import Counter
import pickle
import math
import os
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
    worddict = {i:worddict[i] for i in worddict if worddict[i]>=2 and len(i)>2}
    return worddict

# def createvocab():
    
# def settingdicts():
    # global positive,negative
    

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
        return math.log10((float)(totalpos)/totalreviews)
    else :
        return math.log10((float)(totalneg)/totalreviews)

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
        posprob=math.log10(classconditional(word,'+'))
        negprob=math.log10(classconditional(word,'-'))
        prob[word]=[posprob,negprob]
    pickleout(prob,'classifier')
    # MNB=pickleIn('classifier')
    # outfile=open('classifier.txt','w+')
    # for line in MNB:
    #   outfile.write(line)
    # outfile.close()

def findclasscond(line,classname):
    words=line.split()
    logprob=0
    for word in words:
        logprob+=math.log10(classconditional(word,classname))
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

def clear_all():
    for doc in [pos,neg]:
        for typ  in ['train_']:
            destroy(typ+doc)
    destroy('vocabulary.txt')
    for doc in ['pos_','neg_','vocab_']:
        destroy(doc+'dict.p')

def crossvalidate():
    global negative,positive
    accuracysum=0
    itr=0
    for i in range(1,11):   
        # print str(i)+'\n'
        positive,negative={},{}

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

        poslist=createlist('train_'+pos)
        posdict=createdict(poslist)
        pickleout(posdict,'pos_dict')
        positive=pickleIn('pos_dict')

        outfile=open('positive.txt','w+')
        for word in positive:
            outfile.write(word+':'+str(positive[word])+'\n')
        outfile.close()

        neglist=createlist('train_'+neg)
        negdict=createdict(neglist)
        pickleout(negdict,'neg_dict')
        negative=pickleIn('neg_dict')

        # outfile=open('negative.txt','w+')
        # for i in negative:
        #   outfile.write(i+str(negative[i])+'\n')
        # outfile.close()


        totallist=poslist+neglist
        vocab=createdict(totallist)
        pickleout(vocab,'vocabdict')
        vocablry=pickleIn('vocabdict')
        outfile=open('vocabulary.txt','w+')

        print len(vocablry)


        for word in vocablry:
            outfile.write(word+'\n')

        outfile.close()

        create_model()
        prob=pickleIn('classifier')

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
    tenfold(pos,postotal)
    tenfold(neg,negtotal)
    crossvalidate()

main()