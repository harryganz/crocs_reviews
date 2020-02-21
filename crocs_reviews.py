#!/usr/bin/python

import getopt, sys, csv, subprocess

def main():
    infile=None
    outfile=None
    brands = []

    # Parse options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:i:o:", ["help", "brands=", "infile=", "outfile="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-b", "--brands"):
            brands.append(a)
        elif o in ("-i", "--infile"):
            infile = a
        elif o in ("-o", "--outfile"):
            outfile = a
        else:
            assert False, "unknown option: " + o
    # Exit if missing required options
    if not infile or not outfile or len(brands) == 0:
        print('missing one or more required arguments')
        usage()
        sys.exit(2)
    # Get product list for each brand
    for brand in brands:
        try:
            subprocess.check_call([
                'scrapy',
                'crawl',
                '-a' ,
                'brand={0}'.format(brand),
                '-a',
                'outfile={0}'.format(infile),
                '-a',
                'max_pages={0}'.format(1),
                'amazon_products'
            ])
        except subprocess.CalledProcessError as err:
            print(err)
            sys.exit(2)
    with open(infile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = row['brand']
            product_id = row['product_id']
            product_name = row['product_name']
            try:
                subprocess.check_call([
                    'scrapy',
                    'crawl',
                    '-a',
                    'brand={0}'.format(brand),
                    '-a',
                    'product_id={0}'.format(product_id),
                    '-a',
                    'product_name={0}'.format(product_name),
                    '-a',
                    'outfile={0}'.format(outfile),
                    '-a',
                    'max_pages={0}'.format(1),
                    'amazon_reviews'
                ])
            except subprocess.CalledProcessError as err:
                print(err)
                sys.exit(2)



def usage():
    print("crocs_reviews.py -i <input_file> -o <output_file> -b <brand_name> [-b <brand_name> ...]")


if __name__ == "__main__":
    main()


