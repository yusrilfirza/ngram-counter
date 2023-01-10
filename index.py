#!/usr/bin/python3
import argparse
import numpy as np
import re
import json

def parseFile(filename, variable):
    with open(filename) as file:
        for word in file:
            for string in re.split('; |, |: |\. |\*|\n', word):
                if string != '':
                    variable.append(string)

def findNGram(corpus, cover, result = {}, maxCount = {}):
    start = 0
    n = 2

    arrayCover = np.array(cover)
    arrayCorpus = np.array(corpus)

    while start + n <= len(arrayCover):
        nGramCover = arrayCover[start:start+n]
        index = 0
        while index + n <= len(arrayCorpus):
            nGramCorpus = arrayCorpus[index:index+n]
            if (' '.join(nGramCover) == ' '.join(nGramCorpus)):
                nGram = str(n) + ' gram'
                try:
                    result[' '.join(nGramCorpus)]['freq'] += 1
                    result[' '.join(nGramCorpus)]['percent'] = (result[' '.join(nGramCorpus)]['freq']/maxCount[nGram]) * 100
                except KeyError:
                    result[' '.join(nGramCorpus)] = { 'freq': 1, 'percent': (1/maxCount[nGram]) * 100}
            index += 1
        if (start + n == len(arrayCover)):
            start = 0
            n += 1
        else:
            start += 1
    return result

def findMaxCount(corpus, result = {}):
    start = 0
    n = 2

    while start + n <= len(corpus):
        if (start + n == len(corpus)):
            try:
                result[str(n) + ' gram'] += start
            except KeyError:
                result[str(n) + ' gram'] = start
            start = 0
            n += 1
        start += 1
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-corpus", dest="corpus", type=str, help="Paragraph file")
    parser.add_argument("-cover", dest="cover", type=str, help="Sentence file")
    parser.add_argument("-o", dest="out_file", type=str, help="Output file")

    args = parser.parse_args()
    if args.corpus == None or args.cover == None or args.out_file == None:
        print("Missing mandatory flags -corpus, -cover or -o")
        exit()
    else:
        corpus = []
        cover = []

        parseFile(args.corpus, corpus)
        parseFile(args.cover, cover)
        maxCount = {}
        count = {}

        for corp in corpus:
            maxCount = findMaxCount(corp, maxCount)

        for sentence in cover:
            for corp in corpus:
                count = findNGram(corp.split(), sentence.split(), count, maxCount)
        with open(args.out_file + '.json', 'w') as output:
            json.dump(count, output)

        print(count)
