pos = 'pos2.txt'
neg = 'neg2.txt'



def get_uniq(fname):
	infile = open(fname,'r')
	s = set([])
	count=0
	for line in infile:
		for i in line:
			s = s | set(i)
	print s


def remove_char(fname):
	infile = open(fname,'r')
	outfile = open('temp_'+fname,'w')
	l = [ '"', '&', ',', '.',':','\\', '`', '!', "'", '-', '/',';', '?']
	data=infile.read()
	for char in l:
		data = data.replace(char,"")
	data = data.replace("\n ","\n")
	#write
	outfile.write(data)

def lower(fname):
    infile = open('temp_'+fname,'r')
    outfile = open('lower_'+fname,'w')

    for s in infile:
    	s=s.lower()
    	outfile.write(s)

remove_char(pos)
remove_char(neg)
lower(pos)
lower(neg)