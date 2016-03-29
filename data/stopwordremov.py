pos = 'pos2.txt'
neg = 'neg2.txt'
from collections import Counter


def unique_file(fname):
    infile = open('lower_'+fname, 'r')
    file_contents = infile.read()
    infile.close()
    word_list = file_contents.split()
    s=[]
    outfile = open('unique_'+fname, 'w')
    for word in word_list:
       s.append(word);

    z= Counter(s);
       
    for word in z:
        if z[word]>=2:
         outfile.write(str(word)+' : '+str(z[word])+"\n")
    outfile.close()
unique_file(pos)