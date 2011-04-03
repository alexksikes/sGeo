def run(f):
    for l in open(f):
        l = l.split('\t')
        print '\t'.join(l[0].split('.')) + '\t' + '\t'.join(l[1:])[:-1]
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Usage: python tabbed.py infile"
    else:
        run(sys.argv[1])