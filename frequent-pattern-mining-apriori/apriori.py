"""
Developed by Nicholas Gambirasi - February 8, 2023 - as part of his coursework in association 
with the Unviersity of Illinois at Urbana-Champaign. 
"""

from itertools import combinations
from argparse import ArgumentParser
import time

def apriori(infile: str, relative_support: float, outfile: str) -> None:

    """
    This function is an implementation of the Apriori Algorithm for frequent
    pattern discovery. It takes the following inputs:

        - infile (str): the path to the input file that contains the
        transaction database

        - relative_support (float): the relative decimal support value
        that defines frequency in the transaction database
    
    and produces the following output:

        - outfile (str): filepath to the output file that includes all
        of the frequent patterns in the transaction database

    """

    # assert that the relative support value provided is a decimal value between zero and one

    assert(
        relative_support > 0 and relative_support <= 1
    ), f"Relative support value must be between zero and one, got {relative_support}"


    category_lists = []
    # read the transaction database from the provided input file
    with open(infile, 'r') as f:

        for line in f.readlines():

            l = line.strip().split(";")
            category_lists.append(l)
    
    f.close()

    # compute the absolute support required for an itemset to be frequent
    MIN_ABS_SUPPORT = int(relative_support * len(category_lists))

    # create integer IDs for each distinct category in the file
    item_ids = {} # dictionary to store item IDs
    item_id = 0

    # traverse each list and create ids for items not previously stored
    for li in category_lists:

        for item in li:

            if item not in item_ids.keys():

                item_ids[item] = item_id
                item_id = item_id + 1

    # traverse the list again and map each category to its corresponding ID
    id_lists = []
    for li in category_lists:

        id_list = []

        for item in li:

            i_d = item_ids[item]
            id_list.append(i_d)
        
        id_lists.append(id_list)

    # we traverse the ID lists and generate the frequent one itemsets in the transaction DB
    item_counts = {}

    # count the numer of times each ID appears in the transaction database
    for li in id_lists:

        for i_d in li:

            if i_d not in item_counts.keys():

                item_counts[i_d] = 0

            item_counts[i_d] = item_counts[i_d] + 1

    # filter the counts into a frequent dictionary using the minimum absolute support
    frequent_one_itemsets_ids = []
    frequent_one_itemsets = {}
    for item_count in item_counts.keys():

        count = item_counts.get(item_count)

        if count > MIN_ABS_SUPPORT:

            frequent_one_itemsets_ids.append(item_count)
            frequent_one_itemsets[list(item_ids.keys())[list(item_ids.values()).index(item_count)]] = count

    # we now have the list of the frequent one itemsets, which is necessary to begin the apriori
    # algorithm implementation

    # initialize the frequent itemset list as the frequent one itemsets
    previous_frequent_items = frequent_one_itemsets_ids

    # initialize set length and maximal potential frequent itemset length
    set_length = 2
    MAX_SET_LENGTH = len(previous_frequent_items)

    with open(outfile, 'w') as f:

        for frequent_one_itemset in frequent_one_itemsets.keys():
            
            line = f"{frequent_one_itemset}:{frequent_one_itemsets.get(frequent_one_itemset)}"
            f.write(line)

        while set_length < MAX_SET_LENGTH:

            # create a list for the current frequent itemsets
            current_frequent_itemsets = []

            # check for set length equal to 2
            if set_length == 2:

                candidates = combinations(previous_frequent_items, 2)

            else:

                candidates = frozenset([a.union(b) for a in previous_frequent_items for b in previous_frequent_items if len(a.union(b)) == set_length])

            # iterate through the candidates
            for candidate in candidates:

                candidate = frozenset(candidate)

                # if all of a candidate's subsets are not in the frequent subsets from the previous
                # iteration, proceed to the next candidate
                subsets = combinations(candidate, set_length - 1)
                for subset in subsets:
                    subset = frozenset(subset)
                    if not subset.issubset(candidate):
                        break

                # initialize the count of the number of times a candidate appears in the TDB
                candidate_count = 0

                # iterate through transaction lists and increment counter when candidate appears
                for li in id_lists:

                    if candidate.issubset(li):

                        candidate_count = candidate_count + 1
                    
                # add candidate to frequent itemsets if count is higher than threshold
                if candidate_count > MIN_ABS_SUPPORT:

                    print(f"{list(candidate)} has count {candidate_count}")

                    # create the list of items from the set
                    items = ''

                    for i, item in enumerate(candidate):

                        # get the category string from the table of IDs
                        item = list(item_ids.keys())[list(item_ids.values()).index(item)]

                        if (i != (len(candidate) - 1)):

                            items = items + item + ";"

                        else:

                            items = items + item
                    
                    line = f"{candidate_count}:{items}\n"
                    f.write(line)

                    current_frequent_itemsets.append(candidate)
            
            print(f"\nTotal frequent {set_length}-itemsets: {len(current_frequent_itemsets)}")

            if not len(current_frequent_itemsets):
                break
            
            previous_frequent_items = current_frequent_itemsets
            set_length = set_length + 1

            print(f"Now discovering length {set_length} frequent itemsets...\n")

    f.close()

parser = ArgumentParser()
parser.add_argument('--infile', '-i', action='store', dest='infile', type=str, required=True, default='', help='Path to input file')
parser.add_argument('--min-support', '-s', action='store', dest='min_support', type=float, required=True, default=0.5, help='Minimum relative support value for a frequent pattern, \
    between 0 and 1')
parser.add_argument('--outfile', '-o', action='store', dest='outfile', type=str, required=True, default='', help='Path to output file')

args = parser.parse_args()
INFILE = args.infile
MIN_SUPPORT = args.min_support
OUTFILE = args.outfile

start_time = time.time()

apriori(INFILE, MIN_SUPPORT, OUTFILE)

print(f"\nApriori execution time: {round(time.time()-start_time, 2)} seconds\n")