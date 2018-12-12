#!/usr/bin/env python
#
# _____     _                      _____                             _
#|   | |___| |_ ___ ___ ___ ___   |  _  |___ ___ ___ _ _ _ ___ ___ _| |
#| | | | -_|  _| . | -_| .'|  _|  |   __| .'|_ -|_ -| | | | . |  _| . |
#|_|___|___|_| |_  |___|__,|_|    |__|  |__,|___|___|_____|___|_| |___|
#              |___|
#
#   _____             _               _   _         _
#  |     |___ ___ ___| |_ ___ _ _ ___| |_|_|___ ___| |_ ___ ___
#  |   --| . |   |_ -|  _|  _| | |  _|  _| |   | .'|  _| . |  _|
#  |_____|___|_|_|___|_| |_| |___|___|_| |_|_|_|__,|_| |___|_|   v0.2.0
#                                                                      
# Generates default wifi passwords for Netgear routers
#
# By: Brad Nelson (Squirrel)
# Twitter: @redsquirrel_7
#
# Adjective and Noun files downloaded from: http://www.ashley-bovan.co.uk/words/partsofspeech.html
#
import sys
import subprocess
from binascii import unhexlify

adjectives = []
nouns = []
numbers = []

INPUT_ESSID = ""

lazy_abcs = "abcdefghijklmopqrstuvwxyz"

###TODO: actual leetness
# we'll popen these here with this url, with a length, real EZ
# curl --silent 'https://www.morewords.com/wordsbylength/15a/' > 15.html
# cat 15.html | grep -oE '\/word\/(\w*)\/' |& awk 'FS="/"{print $3;}'

def get_noun_length_spectrum(essid):
    prefix = "MySpectrumWiFi"
    
    if not prefix in essid:
        return 0
    
    hexa_byte = essid[len(prefix)::1]
    hexa_byte = bytes(hexa_byte[0:2])
    ones, teens = int(hexa_byte,16) & 0x0F, int(hexa_byte,16) >> 1
    
    noun_length = ones+teens
    if noun_length > 15:
        noun_length = 15
    
    return noun_length
    

def get_nouns_of_length(len_noun, letter):
    global lazy_abcs
    global nouns
    
    open("{0}.html".format(len_noun), 'a').close()
    
    curled_url = "curl --silent 'https://www.morewords.com/wordsbylength/%d%s' >> %d.html" % (len_noun, lazy_abcs[letter], len_noun)
    words_src = "cat %d.html | grep -oE '\/word\/(\w*)\/' |& awk 'FS=\"/\"{print $3;}'" % len_noun
    
    subprocess.Popen(curled_url, shell=True, executable="/bin/bash")
    
    results = subprocess.Popen(words_src, stdout=subprocess.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)
    
    pulled_nouns = results.stdout.read()
    pulled_nouns = pulled_nouns.split('\n')
    nouns += pulled_nouns
    
    if 'z' in lazy_abcs[letter]:
        return
    
    return get_nouns_of_length(len_noun, letter+1)


# Get the words from adjectives.txt and nouns.txt
def get_words():
    global adjectives
    global nouns
    f = open("adjectives.txt", "r")
    a = f.read()
    adjectives = a.split('\n')
    f.close()
    
    f = open("nouns.txt", "r")
    n = f.read()
    nouns = n.split('\n')
    f.close()

# Generate a list of numbers from 000 to 999
def number_gen():
    global numbers
    number = 0
    while number <= 999:
        if len(str(number)) == 3:
            numbers.append(str(number))
            number += 1
        elif len(str(number)) == 2:
            numbers.append("0" + str(number))
            number += 1
        else:
            numbers.append("00" + str(number))
            number += 1

# Smoosh all of it together into juicy default passwords!
# Uncomment the lines in this function to create a password file
# I do not recommend you do this however...
# The file will be freaking massive!
def smoosh():
    global adjectives
    global nouns
    global numbers
    #f = open("default-netgear-passwords.txt", "w+")  
    for a in adjectives:
        for n in nouns:
            for i in numbers:
                password = str(a) + str(n) + str(i)
                password = password.lower()
                print(password)
                #f.write(password + "\n")
    #f.close()



if len(sys.argv) >= 2:
    INPUT_ESSID = sys.argv[1]

get_nouns_of_length(get_noun_length_spectrum(INPUT_ESSID), 0)

get_words()
number_gen()
smoosh()
