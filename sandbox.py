# This is a sandbox workground to test new features without having to reload the bot all the goddam time
import modules.duolingo_lib
import modules.duolingo_lib as duolingo
from dotenv import load_dotenv
import os

load_dotenv()
DUOLINGO_USER = os.getenv('DUOLINGO_USERNAME')
DUOLINGO_PASS = os.getenv('DUOLINGO_PASSWORD')

# At this point, we want to be able to do the following:
# Find users from a given name
# Add user as a friend (following)
# Get their progress for the day and for the week
# 	- Need Duolingo's reset time
#

lingo = duolingo.Duolingo(DUOLINGO_USER, DUOLINGO_PASS)

user = None
try:
	user = lingo.get_new_user_info("Dynalise1")
except Exception:
	print("Could not get user requested")

if user is not None:
	print("Found " + user['username'] + " with name " + user["fullname"] + ", is this correct?")
	print("Unique ID: " + str(user["id"]))

	print('Streak extended today: ' + str(user['streak_extended_today']))

# print(lingo.get_user_info())


