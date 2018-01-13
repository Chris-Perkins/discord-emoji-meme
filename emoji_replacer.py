import configparser
import discord
from random import randint
from math import ceil

command_prefix = ".em "
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
daddy = "Ȝ"
think = "ʨ"
rod   = "ʤ"
buns  = "Ƞ"
kms   = "ʛ"

special_case_replace_dictionary = {
    "cool" : cool,
    "ok"   : ok,
    "ng"   : ng,
    "new"  : new,
    "abc"  : abc,
    "ab"   : ab,
    "sos"  : sos,
    "cl"   : cl,
    "tm"   : tm,
    "up"   : up,
    "new"  : new,
    "free" : free,
    "end"  : end,
    "back" : back,
    "on"   : on,
    "top"  : top,
    "soon" : soon,
    "<3"   : love,
    "love" : love,
    "luv"  : love,
    "daddy": daddy,
    "think": think,
    "hmmm" : think,
    "hmm"  : think,
    "penis": rod,
    "dick" : rod,
    "cock" : rod,
    "booty": buns,
    "butt" : buns,
    "ass"  : buns,
    "kms"  : kms
}

char_replacement_dictionary = {
    '1'  : [":one:"],
    '2'  : [":two:"],
    '3'  : [":three:"],
    '4'  : [":four:"],
    '5'  : [":five:"],
    '6'  : [":six:"],
    '7'  : [":seven:"],
    '8'  : [":eight:"],
    '9'  : [":nine:"],
    '0'  : [":zero:"],
    'a'  : [":regional_indicator_a:", ":a:"],
    'b'  : [":regional_indicator_b:", ":b:"],
    'c'  : [":regional_indicator_c:", ":star_and_crescent:"],
    'd'  : [":regional_indicator_d:"],
    'e'  : [":regional_indicator_e:"],
    'f'  : [":regional_indicator_f:"],
    'g'  : [":regional_indicator_g:"],
    'h'  : [":regional_indicator_h:"],
    'i'  : [":regional_indicator_i:", ":information_source:"],
    'j'  : [":regional_indicator_j:"],
    'k'  : [":regional_indicator_k:"],
    'l'  : [":regional_indicator_l:"],
    'm'  : [":regional_indicator_m:", ":m:"],
    'n'  : [":regional_indicator_n:"],
    'o'  : [":regional_indicator_o:", ":o:", " :o2:"],
    'p'  : [":regional_indicator_p:"],
    'q'  : [":regional_indicator_q:"],
    'r'  : [":regional_indicator_r:"],
    's'  : [":regional_indicator_s:"],
    't'  : [":regional_indicator_t:"],
    'u'  : [":regional_indicator_u:"],
    'v'  : [":regional_indicator_v:"],
    'w'  : [":regional_indicator_w:"],
    'x'  : [":regional_indicator_x:", ":x:", ":heavy_multiplication_x:",
            ":negative_squared_cross_mark:"],
    'y'  : [":regional_indicator_y:"],
    'z'  : [":regional_indicator_z:"],
    '!'  : [":exclamation:"],
    '?'  : [":question:"],
    '-'  : [":heavy_minus_sign:"],
    '+'  : [":thumbsup:"],
    ok   : [":ok:"],
    ng   : [":ng:"],
    new  : [":new:"],
    ab   : [":ab:"],
    sos  : [":sos:"],
    cl   : [":cl:"],
    abc  : [":abc:"],
    cool : [":cool:"],
    tm   : [":tm:"],
    up   : [":up:"],
    new  : [":new:"],
    free : [":free:"],
    end  : [":end:"],
    back : [":back:"],
    on   : [":on:"],
    top  : [":top:"],
    soon : [":soon:"],
    love : [":heart:", ":hearts:", ":sparkling_heart:", ":heartpulse:"],
    daddy: [":weary: :regional_indicator_d: :a: :regional_indicator_d: :regional_indicator_d:" +
            ":regional_indicator_y: :weary:"],
    think: [":thinking:"],
    rod  : [":eggplant:"],
    buns : [":peach:"],
    kms  : [":grimacing: :gun:", ":sunglasses: :gun:"]
}

def string_to_emoji_message_list(input_string):
    '''
    :param input_string: The string that will parse emojis
    :return: A list of emoji strings whose length does not exceed max message limit
    '''

    input_string = input_string.lower()
    return_messages = list()

    for special_case in special_case_replace_dictionary:
        input_string = input_string.replace(special_case, special_case_replace_dictionary[special_case])

    current_string = ""
    for c in input_string:
        append_string = ""

        if c in char_replacement_dictionary:
            choices = char_replacement_dictionary[c]
            # add an extra space as Discord collapses side-by-side chars like "de" to a flag.
            append_string = choices[randint(0, len(choices) - 1)] + " "
        else:
            append_string = (" " * 4) if c == " " else c

        if len(append_string) + len(current_string) <= max_message_length:
            current_string += append_string
        else:
            return_messages.append(current_string)
            current_string = append_string

    # Make sure to attach the last message since it didn't go over message limit
    return_messages.append(current_string)

    return return_messages


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    client = discord.Client()

    @client.event
    async def on_ready():
        print("Ready to meme!\nEmojify your sentences by starting them with '{0}'".replace("{0}", command_prefix))

    @client.event
    async def on_message(message):
        if message.author.id == config["user"]["id"] and message.content.startswith(command_prefix):
            await client.delete_message(message)


            emoji_messages = string_to_emoji_message_list(message.content[len(command_prefix):])
            for emoji_message in emoji_messages:
                await client.send_message(message.channel, emoji_message)

    print("Logging in, please wait...")
    client.run(config["user"]["token"], bot=False)


if __name__ == "__main__":
    main()
