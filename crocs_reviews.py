#!/usr/bin/python

import getopt, sys, csv, subprocess
from datetime import date

def main():
    infile=None
    outfile=None
    current_date = date.today().strftime("%d-%m-%Y")

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
    with open(infile, newline='') as itemsfile:
        itemsreader = csv.DictReader(itemsfile)
        for row in itemsreader:
            try:
                filename = '{}-{}-{}.csv'.format(row['product_name'], row['product_id'], current_date)
                print("filename " + filename)
                subprocess.check_call(['scrapy', 'crawl', 'amazon_reviews', '-a', 'product_id={}'.format(row['product_id']), '-o', filename])
            except subprocess.CalledProcessError as err:
                print(err)
                sys.exit(2)

def usage():
    print("crocs_reviews.py -i <input_file> -o <output_file>")


if __name__ == "__main__":
    main()


