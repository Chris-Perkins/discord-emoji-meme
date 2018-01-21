import configparser
import discord
from random import randint

emoji_command_prefix = ".em "
clap_command_prefix  = ".clap "
react_command_prefix = ".react "
max_message_length = 2000

# replacements ordered by length
# so longer phrases get replaced. Please format new entries appropriately.
special_case_replace_dictionary = {
    "booty": "🍑",
    "daddy": "😩" + "daddy" + "😩",
    "hmmmm": "🤔",
    "penis": "🍆",
    "think": "🤔",

    "back": "🔙",
    "butt": "🍑",
    "cock": "🍆",
    "cool": "🆒",
    "dick": "🍆",
    "free": "🆓",
    "hmmm": "🤔",
    "love": "😍",
    "soon": "🔜",

    "abc": "🔤",
    "ass": "🍑",
    "end": "🔚",
    "hmm": "🤔",
    "kms": "😀" + "🔫",
    "luv": "😍",
    "new": "🆕",
    "sos": "🆘",
    "top": "🔝",

    "<3": "😍",
    "ab": "🆎",
    "cl": "🆑",
    "ng": "🆖",
    "ok": "🆗",
    "on": "🔛",
    "tm": "™",
    "up": "🆙"
}


# Char -> Emoji replacements should be done here
char_replacement_dictionary = {
    "😀": ["😬", "😎", "😩"],
    "😍": ["❤", "💕", "💖", "💗"],
    '#': ["#⃣"],
    '1': ["1⃣"],
    '2': ["2⃣"],
    '3': ["3⃣"],
    '4': ["4⃣"],
    '5': ["5⃣"],
    '6': ["6⃣"],
    '7': ["7⃣"],
    '8': ["8⃣"],
    '9': ["9⃣"],
    '0': ["0⃣"],
    'a': ["🇦", "🅰"],
    'b': ["🇧", "🅱"],
    'c': ["🇨", "☪"],
    'd': ["🇩"],
    'e': ["🇪"],
    'f': ["🇫"],
    'g': ["🇬"],
    'h': ["🇭"],
    'i': ["🇮", "ℹ"],
    'j': ["🇯"],
    'k': ["🇰"],
    'l': ["🇱"],
    'm': ["🇲", "Ⓜ"],
    'n': ["🇳"],
    'o': ["🇴", "🅾", "⭕"],
    'p': ["🇵"],
    'q': ["🇶"],
    'r': ["🇷"],
    's': ["🇸"],
    't': ["🇹"],
    'u': ["🇺"],
    'v': ["🇻"],
    'w': ["🇼"],
    'x': ["🇽", "✖", "❌", "❎"],
    'y': ["🇾"],
    'z': ["🇿"],
    '!': ["❗"],
    '?': ["❓"],
    '-': ["➖"],
    '+': ["👍"]
}


# replaces replaceable characters with emojis
def string_to_emoji_message_list(input_string, reacting=False):
    '''
    :param input_string: The string that we will be parsing for emoji replacements
    :param random: whether or not this should be random
    :return: A list of emoji strings whose length does not exceed max message limit if not reacting
            if reacting, a list of len = 1 containing one string
    '''

    input_string = input_string.lower()
    return_messages = list()
    letter_occurrences_dict = {}

    for special_case in special_case_replace_dictionary:
        if reacting:
            input_string = input_string.replace(special_case, special_case_replace_dictionary[special_case], 1)
        else:
            input_string = input_string.replace(special_case, special_case_replace_dictionary[special_case])

    # the current word we're parsing (not interrupted by "\n" or " ")
    current_word = ""
    # the current string we'll append to return message
    current_string = ""

    for c in input_string:
        append_string = ""

        if c == " " or c == "\n":
            spacing_string = (" " * 4) if c == " " else "\n"

            # if the resulting string would be greater than the limit,
            # break so that we don't cause an exception
            if len(current_word) + len(current_string) + len(spacing_string) > max_message_length:
                return_messages.append(current_string)
                current_string = ""

            # add to the resulting string and reset the word
            current_string += current_word + spacing_string
            current_word = ""

        elif c in char_replacement_dictionary:
            choices = char_replacement_dictionary[c]
            if not reacting:
                # add an extra space as Discord collapses side-by-side chars like "de" to a flag.
                append_string = choices[randint(0, len(choices) - 1)] + " "
            else:
                if c not in letter_occurrences_dict:
                    letter_occurrences_dict[c] = 0
                if letter_occurrences_dict[c] == len(choices):
                    raise Exception("Could not react; too many required characters but not enough emojis!")

                append_string = choices[letter_occurrences_dict[c]]
                letter_occurrences_dict[c] += 1

        else:
            append_string = c + " " if c in special_case_replace_dictionary.values() else c

        # checks if the word itself > the limit. If it is, chop the word up.
        # if it's not, we can just add it to the current word
        if len(append_string) + len(current_word) > max_message_length and not reacting:
            return_messages.append(current_word)
            current_word = ""

        current_word += append_string


    # Make sure to attach the last message since it didn't go over message limit
    # chop up from the word as necessary.
    if len(current_word) + len(current_string) <= max_message_length or reacting:
        return_messages.append(current_string + current_word)
    else:
        return_messages.append(current_string)
        return_messages.append(current_word)

    return return_messages


# replaces spaces with :clap: and doesn't go over the message char limit
def message_to_clappified_message_list(input_string):
    '''
    :param input_string: The string to clappify
    :return: a list of messages with all spaces in input_string replaced with :clap:
    '''
    
    return_messages = list()

    current_message = ""
    for c in input_string:
        append_string = ":clap:" if c == " " else c

        if len(current_message) + len(append_string) > max_message_length:
            return_messages.append(current_message)
            current_message = ""

        current_message += append_string

    # attach the last string since it didn't go over the limit
    return_messages.append(current_message)

    return return_messages


# returns the message from client if possible
def get_message_with_id(client, msg_id):
    '''
    :param client: The discord client to parse from
    :param id: the id of the message to parse
    :return: the message we want (must be from the past 5k messages and be sent after client start)
    '''
    for message in client.messages:
        if message.id == msg_id:
            return message
    else:
        raise Exception("Message with id %s could not be found or was from the past." % msg_id)


# parses the id and msg from some string
def get_id_and_content_from_str(input_string):
    '''
    :param input_string: the string to parse id and message from
    :return: the id and message content if possible. None if improperly formatted
    '''
    space_separated = input_string.split()

    if len(space_separated) > 1:
        msg_id = space_separated[0]
        return msg_id, input_string[len(msg_id):]
    else:
        raise Exception("react command improperly formatted; could not find id or message.")


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    client = discord.Client()

    @client.event
    async def on_ready():
        print("Ready to meme!\n" +
              ("'%s [message]' - Emojify a message\n" % emoji_command_prefix) +
              ("'%s [message]' - Clappify a message\n" % clap_command_prefix) +
              ("'%s [message_id] [message]' - Reacts to message with id '[message_id]' with [message]" %
               react_command_prefix))

    @client.event
    async def on_message(message):
        user_is_owner = message.author.id == config["user"]["id"]

        if user_is_owner:
            if message.content.startswith(emoji_command_prefix):
                await client.delete_message(message)

                emoji_messages = string_to_emoji_message_list(message.content[len(emoji_command_prefix):])
                for emoji_message in emoji_messages:
                    await client.send_message(message.channel, emoji_message)
            elif message.content.startswith(clap_command_prefix):
                await client.delete_message(message)

                clappified_messages = message_to_clappified_message_list(message.content[len(clap_command_prefix):])

                for clappified_message in clappified_messages:
                    await client.send_message(message.channel, clappified_message)

            elif message.content.startswith(react_command_prefix):
                await client.delete_message(message)

                msg_wo_command = message.content[len(react_command_prefix):]

                react_msg_id, msg_content = get_id_and_content_from_str(msg_wo_command)
                msg_content = msg_content.replace(" ", "").replace("\n", "")

                msg_for_reacting = get_message_with_id(client, react_msg_id)

                reaction_messages = string_to_emoji_message_list(msg_content, reacting=True)
                for reaction_message in reaction_messages:
                    for reaction in reaction_message:
                        try:
                            await client.add_reaction(msg_for_reacting, reaction)
                        except discord.HTTPException:
                            print("'%s' was attempted to be a reaction, but does not exist as emoji" % reaction)



    print("Logging in, please wait...")
    client.run(config["user"]["token"], bot=False)


if __name__ == "__main__":
    main()
