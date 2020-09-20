# Python library designed to handle messages

import discord


# Test function to make sure the library is linked
def test_function():
    print("test")


# Function called to handle commands
def handle_command(message):
    # Filter out the command from the contents
    print(message.content[1:].split(" ")[0].lower())


