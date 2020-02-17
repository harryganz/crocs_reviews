#!/usr/bin/python

import getopt, sys

def main():
    infile=None
    outfile=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "infile=", "outfile="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--infile"):
            infile = a
        elif o in ("-o", "--outfile"):
            outfile = a
        else:
            assert False, "unknown option: " + o

    print(infile)
    print(outfile)

def usage():
    print("crocs_reviews.py -i <input_file> -o <output_file>")


if __name__ == "__main__":
    main()


