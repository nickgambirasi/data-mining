"""
Developed by Nicholas Gambirasi - February 17, 2023 - as part of his coursework in association 
with the Unviersity of Illinois at Urbana-Champaign. 
"""

from collections import Counter
from argparse import ArgumentParser
import time

def modified_gsp(infile: str, relative_support: float, outfile: str) -> None:

    """
    This function is a modified implementation of the GSP Algorithm for frequent contiguous sequential
    pattern discovery. It takes the following inputs:
    
        - infile (str): the path to the input file that contains the 
        text data
        
        - relative_support (float): the relative decimal support value
        that defines frequency within the provided text data
        
    and produces the following output:
    
        - outfile (str): the path to the output file that contains
        all of the frequent patterns in the text database
        
    """

    # we begin by asserting that the relative support value provided is a decimal value between zero and one
    assert(
        relative_support > 0 and relative_support <= 1
    ), f"Relative support value must be between zero and one, got {relative_support}"

    # after asserting that our relative support value is properly given, we process the reviews into lists
    review_lists = []
    with open(infile, 'r') as f:

        for line in f.readlines():

            l = line.strip().split(" ")
            review_lists.append(l)

    f.close()

    # after reading in the reviews, we calculate the minimum absolute support using the relative support
    MIN_ABS_SUPPORT = int(relative_support*len(review_lists))

    # we now map each different word in the text data to a unique integer ID to make set logic simpler
    word_ids = {}
    word_id = 0 # incremental word id value

    for lst in review_lists:

        for word in lst:

            # if word is not in the dictionary, add it with the current id value, then increment the
            # id value
            if word not in word_ids:

                word_ids[word] = word_id
                word_id += 1

    # after assigning each word a unique ID, we create new lists for the reviews using those integer
    # values
    integer_reviews = []

    for lst in review_lists:

        integer_review = []
        
        for word in lst:

            i_d = word_ids[word]
            integer_review.append(i_d)

        integer_reviews.append(integer_review)

    # we now find all of the frequent patterns and write them to the output file

    length = 1 # initialize current length of desired phrases

    with open(outfile, 'w') as f:

        while True:

            print(f"\nSearching for frequent {length}-word phrases...\n")

            frequent_phrase_count = 0
            phrases = []

            # construct a phrase set for each phrase and merge them all into
            # a large list for counting
            for lst in integer_reviews:

                list_phrases = set()

                for i in range(len(lst) - (length - 1)):

                    phrase = tuple(lst[i:(i+length)])
                    list_phrases.add(phrase)

                for phrase in list_phrases:

                    phrases.append(phrase)

            # count the frequency of each phrase
            phrase_counts = Counter(phrases)

            # iterate through the counter to get the frequent itemsets
            for phrase in phrase_counts.keys():

                count = phrase_counts[phrase]

                if count > MIN_ABS_SUPPORT:

                    frequent_phrase_count += 1

                    words = ''

                    for i, i_d in enumerate(phrase):

                        word = list(word_ids.keys())[list(word_ids.values()).index(i_d)]

                        if i != length - 1:

                            words = words + word + ";"

                        else: 

                            words = words + word

                    line = f"{count}:{words}\n"
                    f.write(line)

            print(f"Total frequent {length}-word phrases: {frequent_phrase_count}")

            if not frequent_phrase_count:
                break

            length += 1

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

modified_gsp(INFILE, MIN_SUPPORT, OUTFILE)

print(f"\nExecution time: {round(time.time()-start_time, 2)} seconds\n")