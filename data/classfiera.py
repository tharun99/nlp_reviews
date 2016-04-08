import pickle
from collections import Counter
import math
import fileinput
import os

pos = 'pos2.txt'
neg = 'neg2.txt'

negative,postive,vocabulary={},{},{}
voc_size=0


# def editfiles(fname):
#     for line in fileinput.FileInput(fname,inplace=1):
#         if line.rstrip():
#             print line
def destroy(fname):
    if os.path.exists(fname):
        os.remove(fname)
def clear_all():
    for doc in [pos,neg]:
        # for i in range(1,11):
        #     destroy(str(i)+doc)
        for typ  in ['temp_','train_']:
            destroy(typ+doc)
    destroy('vocabulary.txt')
    for doc in ['pos_','neg_','vocab_']:
        destroy(doc+'dict.p')


def replace_char(fname):
    infile = open(fname,'r')
    outfile = open('temp_'+fname,'w')
    l = ['"', '&', ',', '.', ':','\\', '`', '!', "'", '-', '/',';', '?','$', '*',]
    data=infile.read()
    for char in l:
        data = data.replace(char,"")
    data = data.replace("\n ","\n")

    num='0123456789'

    for i in num:
        data=data.replace(i,"")
    #write
    outfile.write(data)

def lower(fname):
    infile = open('temp_'+fname,'r')
    data=infile.read()
    data=data.lower()
    outfile = open('temp_'+fname,'w')
    outfile.write(data)

name_list=[]
def read_names():
    with open('stopwords.txt','r') as f:
        name_list=[line.strip() for line in f]
        # print name_list
    return (name_list)


def  removestopwords(fname):
    name_list=read_names()
    infile = open(fname, 'r')
    file_contents = infile.read()
    infile.close()
    word_list = file_contents.split()
    s=[]
    # print (name_list)
    for word in word_list:
        if word not in name_list:
            s.append(word)
    # print s
    return s

def createdict(s):
    counts = Counter(s)
    counts = {i:counts[i] for i in counts if counts[i]>=2}
    return counts


def pickleout(temp,fname):
    pickle_out = open(fname+'.p', 'wb')
    pickle.dump(temp, pickle_out)
    pickle_out.close()

def pickleIn(fname):
    pickle_in = open(fname+'.p','rb')
    db1 = pickle.load(pickle_in)    
    return db1

def sumoffreq(dt):
    count=0
    for word in dt:
        count+=dt[word]
    return count

def p(word,clss):
    global negative,postive,vocabulary,voc_size

    if(clss==1) :
    # 1 for positive
        dt=positive
    else:
        dt=negative

    classcount=sumoffreq(dt)

    if word in dt:
        return math.log10(dt[word])-math.log10(voc_size+classcount)
    else :
        return math.log10(1)-math.log10(voc_size+classcount)


def create_model():
    global negative,positive,vocabulary,voc_size,prob
    #here i made mistake bakayaro
    prob={}
    for word in vocabulary:
        prob[word]=[p(word,0),p(word,1)]
    pickleout(prob,'MNB')

def q(doc,clss):
    global negative,positive,vocabulary,voc_size,prob
    result=0
    if(clss==1) :
    # 1 for positive
        dt=positive
    else:
        dt=negative

    classcount=sumoffreq(dt)
    doc=doc.split()
    for word in doc:
        if word in vocabulary:
            result+=prob[word][clss]
        else:
            result+=math.log10(1)-math.log10(voc_size+classcount+1)

    return result

def predict(doc):
    if q(doc,1)>q(doc,0):
        return 1
    else:
        return 0

def tenfold(doc):
    infile=open('temp_'+doc)

    for i in range(1,11):
        outfile=open(str(i)+doc,'a')
        for j in range(80):
            outfile.write(infile.readline())
        outfile.close()

def splitting():
    poslist=removestopwords('train_'+pos)
    # print poslist
    posdict=createdict(poslist)
    pickleout(posdict,'pos_dict')
    neglist=removestopwords('train_'+neg)
    negdict=createdict(neglist)
    pickleout(negdict,'neg_dict')
    vocablist= poslist+neglist
    vocabdict= createdict(vocablist)
    pickleout(vocabdict,'vocab_dict')

def clean():
    for f in ['pos_','neg_','vocab_']:
        os.remove(f+'dict.p')

    for f in ['train_'+pos,'train_'+neg,'MNB.p']:
        os.remove(f)

def crossvalidate():
    global negative,positive,vocabulary,voc_size,prob
    accuracysum=0
    itr=0
    for i in range(1,11):
   
        positive,negative,vocabulary,prob={},{},{},{}

        posfreq=0
        negfreq=0
        voc_size=0

        postrain,negtrain='',''

        for j in range(1,11):

            if j!=i:
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

        splitting()

        positive=pickleIn('pos_dict')
        #print positive
        negative=pickleIn('neg_dict')
        vocabulary=pickleIn('vocab_dict')
        # print vocabulary

        posfreq=sumoffreq(positive)
        negfreq=sumoffreq(negative)
        voc_size=len(vocabulary)
        
        create_model()
        prob=pickleIn('MNB')

        fpos,fneg,tpos,tneg=0,0,0,0

        possample=open(str(i)+pos,'r').read().split('\n')
        #print possample
        for doc in possample:
            if doc != '':
                if predict(doc)==1:
                        tpos +=1
                else:
                        fneg +=1

            #print predict(doc)

        negsample=open(str(i)+neg,'r').read().split('\n')

        for doc in negsample:
            if predict(doc)==0:
                tneg +=1
            else:
                fpos +=1
            #print predict(doc)


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
    # editfiles(pos)
    # editfiles(neg)

    # replace_char(pos)
    # replace_char(neg)
    # lower(pos)
    # lower(neg)
    # name_list=read_names()
    # tenfold(pos)
    # tenfold(neg)
    # read_names()
    crossvalidate()
    clear_all()


main()