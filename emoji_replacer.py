import configparser
import discord
from random import randint

emoji_command_prefix = ".em "
clap_command_prefix  = ".clap "
max_message_length = 2000


ok    = "•"
ng    = "‣"
new   = "◦"
ab    = "※"
sos   = "Ŷ"
cl    = "ƈ"
abc   = "Ɔ"
cool  = "Ť"
tm    = "ƌ"
up    = "Ʊ"
new   = "ƞ"
free  = "ƒ"
end   = "Ɛ"
back  = "Ɓ"
on    = "ơ"
top   = "Ƭ"
soon  = "ƨ"
love  = "ǽ"
think = "ʨ"
rod   = "ʤ"
buns  = "Ƞ"
face  = "ʛ"
weary = "Ѻ"
gun   = "Ջ"


# replacements ordered by length
# so longer phrases get replaced. Please format new entries appropriately.
special_case_replace_dictionary = {
    "booty": buns,
    "daddy": weary + "daddy" + weary,
    "hmmmm": think,
    "penis": rod,
    "think": think,

    "back": back,
    "butt": buns,
    "cock": rod,
    "cool": cool,
    "dick": rod,
    "free": free,
    "hmmm": think,
    "love": love,
    "soon": soon,

    "abc": abc,
    "ass": buns,
    "end": end,
    "hmm": think,
    "kms": face + gun,
    "luv": love,
    "new": new,
    "sos": sos,
    "top": top,

    "<3": love,
    "ab": ab,
    "cl": cl,
    "ng": ng,
    "ok": ok,
    "on": on,
    "tm": tm,
    "up": up
}


# please keep any new entries matched up with length of key
# done purely for formatting reasons.
char_replacement_dictionary = {
    think: [":thinking:"],
    weary: [":weary:"],

    back: [":back:"],
    buns: [":peach:"],
    cool: [":cool:"],
    face: [":grimacing:", ":sunglasses:", ":weary:"],
    free: [":free:"],
    love: [":heart:", ":hearts:", ":sparkling_heart:", ":heartpulse:"],
    soon: [":soon:"],

    abc: [":abc:"],
    end: [":end:"],
    gun: [":gun:"],
    new: [":new:"],
    rod: [":eggplant:"],
    sos: [":sos:"],
    top: [":top:"],

    ab: [":ab:"],
    cl: [":cl:"],
    ng: [":ng:"],
    on: [":on:"],
    ok: [":ok:"],
    tm: [":tm:"],
    up: [":up:"],

    '1': [":one:"],
    '2': [":two:"],
    '3': [":three:"],
    '4': [":four:"],
    '5': [":five:"],
    '6': [":six:"],
    '7': [":seven:"],
    '8': [":eight:"],
    '9': [":nine:"],
    '0': [":zero:"],
    'a': [":regional_indicator_a:", ":a:"],
    'b': [":regional_indicator_b:", ":b:"],
    'c': [":regional_indicator_c:", ":star_and_crescent:"],
    'd': [":regional_indicator_d:"],
    'e': [":regional_indicator_e:"],
    'f': [":regional_indicator_f:"],
    'g': [":regional_indicator_g:"],
    'h': [":regional_indicator_h:"],
    'i': [":regional_indicator_i:", ":information_source:"],
    'j': [":regional_indicator_j:"],
    'k': [":regional_indicator_k:"],
    'l': [":regional_indicator_l:"],
    'm': [":regional_indicator_m:", ":m:"],
    'n': [":regional_indicator_n:"],
    'o': [":regional_indicator_o:", ":o:", " :o2:"],
    'p': [":regional_indicator_p:"],
    'q': [":regional_indicator_q:"],
    'r': [":regional_indicator_r:"],
    's': [":regional_indicator_s:"],
    't': [":regional_indicator_t:"],
    'u': [":regional_indicator_u:"],
    'v': [":regional_indicator_v:"],
    'w': [":regional_indicator_w:"],
    'x': [":regional_indicator_x:", ":x:", ":heavy_multiplication_x:",
            ":negative_squared_cross_mark:"],
    'y': [":regional_indicator_y:"],
    'z': [":regional_indicator_z:"],
    '!': [":exclamation:"],
    '?': [":question:"],
    '-': [":heavy_minus_sign:"],
    '+': [":thumbsup:"]
}


# replaces replaceable characters with emojis
def string_to_emoji_message_list(input_string):
    '''
    :param input_string: The string that we will be parsing for emoji replacements
    :return: A list of emoji strings whose length does not exceed max message limit
    '''

    input_string = input_string.lower()
    return_messages = list()

    for special_case in special_case_replace_dictionary:
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
            # add an extra space as Discord collapses side-by-side chars like "de" to a flag.
            append_string = choices[randint(0, len(choices) - 1)] + " "

        else:
            append_string = c

        # checks if the word itself > the limit. If it is, chop the word up.
        # if it's not, we can just add it to the current word
        if len(append_string) + len(current_word) > max_message_length:
            return_messages.append(current_word)
            current_word = ""

        current_word += append_string


    # Make sure to attach the last message since it didn't go over message limit
    # chop up from the word as necessary.
    if len(current_word) + len(current_string) <= max_message_length:
        return_messages.append(current_string + current_word)
    else:
        return_messages.append(current_string)
        return_messages.append(current_word)

    return return_messages


# replaces spaces with :clap: and doesn't go over the message char limit
def message_to_clappified_message_list(input_string):
    '''
    :param input_string: The string that will for
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


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    client = discord.Client()

    @client.event
    async def on_ready():
        print("Ready to meme!\nEmojify your sentences by starting them with '%s' or clappify it using '%s'." %
              (emoji_command_prefix, clap_command_prefix))

    @client.event
    async def on_message(message):
        user_is_owner = message.author.id == config["user"]["id"]

        if user_is_owner and message.content.startswith(emoji_command_prefix):
            await client.delete_message(message)

            emoji_messages = string_to_emoji_message_list(message.content[len(emoji_command_prefix):])
            for emoji_message in emoji_messages:
                await client.send_message(message.channel, emoji_message)
        elif user_is_owner and message.content.startswith(clap_command_prefix):
            await client.delete_message(message)

            clappified_messages = message_to_clappified_message_list(message.content[len(clap_command_prefix):])

            for clappified_message in clappified_messages:
                await client.send_message(message.channel, clappified_message)

    print("Logging in, please wait...")
    client.run(config["user"]["token"], bot=False)


if __name__ == "__main__":
    main()
