pos = 'pos2.txt'
neg = 'neg2.txt'
from collections import Counter

name_list=[]

def read_names():
    with open('stopwords.txt','r') as f:
        name_list=[line.strip() for line in f]
    return (name_list)


def unique_file(fname):
    infile = open('lower_'+fname, 'r')
    file_contents = infile.read()
    infile.close()
    word_list = file_contents.split()
    s=[]
    # print (name_list)
    for word in word_list:
        if word not in name_list:
            s.append(word);
       
    # for word in z:
    #     if z[word]>=2:
    #      outfile.write(str(word)+' : '+str(z[word])+"\n")
    return s
    
    # outfile.close()


name_list=read_names()
poslist=unique_file(pos)
neglist=unique_file(neg)
vocab_list= poslist+neglist

vocab_dict= Counter(vocab_list)

outfile = open('vocabulary.txt', 'w')
for word in vocab_dict:
    if vocab_dict[word]>=2:
        outfile.write(str(word)+"\n")



