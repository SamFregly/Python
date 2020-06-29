import sys
import json
#from pdb import *;
if len(sys.argv) > 1:
    line_generator = open(sys.argv[1])
else:
    line_generator = sys.stdin

#set_trace();
for line in line_generator:

    line_object = json.loads(line)
    try:
        text = line_object["text"]
        #location = line_object["location"]
	#retweets = line_object["retweet_count"]
	#favorites= line_object["user"]["favourites_count"]
    except KeyError, e:
        text= "invalid"
        #location = "the moon"
	#retweets = 0
	#favorites = 0
    print_string = "{0:140s}".format(text)
    print(print_string)
