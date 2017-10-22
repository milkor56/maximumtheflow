import sys

def log(message):
    print(message)
    f = open(sys.argv[0]+".log", 'a')
    f.write("%s\n" % message)
    f.close()