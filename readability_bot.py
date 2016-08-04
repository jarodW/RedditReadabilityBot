import praw
import time
import re
import os
from readability_tools import computeIndex
from config import *

USERNAME = REDDIT_USERNAME
PASSWORD = REDDIT_PASS
user_agent = BOT_NAME
r = praw.Reddit(user_agent=user_agent)
r.login(USERNAME,PASSWORD)

def handle_ratelimit(func, *args):
    while True:
        try:
            func(*args)
            break
        except praw.errors.RateLimitExceeded as error:
            print ('\tRate Limit Error: Sleeping for %d seconds' % error.sleep_time)
            time.sleep(error.sleep_time)

if not os.path.isfile("repliedTo.txt"):
    repliedTo = set()	
else:
    with open("repliedTo.txt", "r") as f:
        text = f.read()
        repliedTo = set()
        repliedTo = set(text.split("\n"))

while(True):		
	for mention in r.get_mentions():
		if mention.new is not False:
			#print(vars(mention))
			parent = r.get_info(thing_id=mention.parent_id)
			if parent.id not in repliedTo:
				if isinstance(parent, praw.objects.Comment):
					print("comment")
					result = computeIndex(parent.body)
					print(parent.body)
					print(result)
					handle_ratelimit(parent.reply, result)
					#parent.reply(result)
				elif isinstance(parent, praw.objects.Submission) and parent.selftext != '':
					result = computeIndex(parent.selftext)
					print("submission")
					print(parent.selftext)
					print(result)
					handle_ratelimit(parent.add_comment, result)
					#parent.add_comment(result)
			mention.mark_as_read()
			repliedTo.add(parent.id)
	with open("repliedTo.txt","w") as f:
		for post_id in set(repliedTo):
			f.write(post_id + "\n")
        
	time.sleep(5);

# with open("repliedTo.txt", "w") as f:
    # for post_id in set(repliedTo):
        # print (post_id)
        # f.write(post_id + "\n")

