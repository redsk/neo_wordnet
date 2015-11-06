import cPickle as pickle
import sys

def main():
    numargs = len(sys.argv)
    w = None
    if numargs == 2:
        fname = sys.argv[1]
    else:
        fname = "../wordnet/WNedges.csv"

    relsSet = set()
    with open (fname, "r") as f:
        for idx, line in enumerate(f):
            if idx == 0:
                continue
            relType = line[0:-1].split('\t')[2][1:-1] # last field, removing commas
            relsSet.add(relType)

    pickle.dump( relsSet, open("../wordnet/relsSet.p", "wb") )

if __name__ == "__main__":
    main()