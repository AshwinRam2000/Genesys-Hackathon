from textblob import TextBlob
from textblob import Word
import sys
from similar import get_cosine, text_to_vector


def parse(string):
    global verbose
    verbose = False
    ques = []
    sim = []
    line = []
    print("hi")
    try:

        txt = TextBlob(string)
        for sentence in txt.sentences:
            q, l = genQuestion(sentence)
            ques.append(q)
            line.append(str(l))

            # sim.append(cosine)
            # print(cosine)

        for q in ques:
            for l in line:
                vector1 = text_to_vector(str(l))
                vector2 = text_to_vector(q)
                sim = get_cosine(vector1, vector2)
                if (sim > 0.5):
                    line.append(l)

    except Exception as e:
        raise e
    print(ques)
    return ques, line


def newline(string, n):
    print(n)
    global verbose
    verbose = False
    ques = []
    sim = []
    line = []
    res = ""
    print("hi")
    try:

        txt = TextBlob(string)
        for sentence in txt.sentences:
            q, l = genQuestion(sentence)
            ques.append(q)
            line.append(str(l))

            # sim.append(cosine)
            # print(cosine)

        for l in line:
            print(l)
            vector1 = text_to_vector(str(l))
            vector2 = text_to_vector(str(n))
            sim = get_cosine(vector1, vector2)
            print(sim)
            if (sim > 0.3):
                res = l
                print(res)

    except Exception as e:
        raise e
    # print(ques)
    return res


def genQuestion(line):

    if type(line) is str:  
        line = TextBlob(line)  

    bucket = {}

    for i, j in enumerate(line.tags):  
        if j[1] not in bucket:
            bucket[j[1]] = i

    if verbose:               
        print('\n', '-'*20)
        print(line, '\n')
        print("TAGS:", line.tags, '\n')
        print(bucket)

    question = ''
    # NNS     Noun, plural
    # JJ  Adjective
    # NNP     Proper noun, singular
    # VBG     Verb, gerund or present participle
    # VBN     Verb, past participle
    # VBZ     Verb, 3rd person singular present
    # VBD     Verb, past tense
    # IN      Preposition or subordinating conjunction
    # PRP     Personal pronoun
    # NN  Noun, singular or mass

    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']

    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']

    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']

    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']
    l14 = ['NNP']       # when is
    l15 = ['DT', 'JJ', 'NNP']  # when is
    l16 = ['PRP$', 'NN']  # when is
    l17 = ['DT', 'NN', 'VBG']  # when is
    l18 = ['DT', 'JJS', 'NN']  # where is
    l19 = ['NNP', 'POS', 'NN']
    l20 = ['NNP', 'POS', 'JJS', 'NN']
    l21 = ['NNS', 'VB']
    l22 = ['DT', 'NN', 'VB']
    l23 = ['NN', 'IN', 'NNP']
    l24 = ['JJ', 'VBZ', 'NNP']
    l25 = ['DT', 'JJS', 'NNS']
    l26 = ['JJR']
    l27 = ['DT', 'JJR', 'NN']
    l28 = ['NN', 'VBZ', 'JJR']
    l29 = ['DT', 'JJR', 'CD']
    l30 = ['NNP', 'POS', 'NNP']
    l31 = ['DT', 'JJ', 'NN']
    l32 = ['PRP$', 'NN']
    l33 = ['DT', 'NN', 'JJ']
    l34 = ['NNP', 'VBN']
    l35 = ['NN', 'VBN']
    l36 = ['NN', 'JJ']
    if all(key in bucket for key in l1):
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + \
            line.words[bucket['NNP']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l2):  # 'NNP', 'VBG', 'VBZ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + \
            line.words[bucket['NNP']] + ' ' + line.words[bucket['VBG']] + '?'
    elif all(key in bucket for key in l3):
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + \
            line.words[bucket['PRP']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l4):  # 'PRP', 'VBG', 'VBZ' in sentence.
        question = 'What ' + line.words[bucket['PRP']] + ' ' + ' does ' + \
            line.words[bucket['VBG']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l7):  # 'NN', 'VBG', 'VBZ' in sentence.
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + \
            line.words[bucket['NN']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l8):  # 'NNP', 'VBZ', 'JJ' in sentence.
        question = 'What' + ' ' + \
            line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l9):  # 'NNP', 'VBZ', 'NN' in sentence
        question = 'What' + ' ' + \
            line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l11):  # 'PRP', 'VBZ' in sentence.
        if line.words[bucket['PRP']] in ['she', 'he']:
            question = 'What' + ' does ' + \
                line.words[bucket['PRP']].lower() + ' ' + \
                line.words[bucket['VBZ']].singularize() + '?'

    elif all(key in bucket for key in l10):  # 'NNP', 'VBZ' in sentence.
        question = 'What' + ' does ' + \
            line.words[bucket['NNP']] + ' ' + \
            line.words[bucket['VBZ']].singularize() + '?'

    elif all(key in bucket for key in l13):  # 'NN', 'VBZ' in sentence.
        question = 'What' + ' ' + \
            line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l4):
        question = 'When' + ' is ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l15):
        question = 'When' + ' is ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['JJ']] + ' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l16):
        question = 'When' + ' is ' + \
            line.words[bucket['PRP$']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l17):
        question = 'When' + ' is ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['NN']] + ' ' + line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l18):
        question = 'Where' + ' is ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['JJS']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l19):
        question = 'Where' + ' is ' + line.words[bucket['NNP']] + ' ' + \
            line.words[bucket['POS']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l20):
        question = 'Where' + ' is ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['POS']
                                                                                   ] + ' ' + line.words[bucket['JJS']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l21):
        question = 'How' + ' do ' + \
            line.words[bucket['NNS']] + ' ' + line.words[bucket['VB']] + '?'

    elif all(key in bucket for key in l22):
        question = 'How' + ' do ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['NN']]+' ' + line.words[bucket['VB']] + '?'

    elif all(key in bucket for key in l23):
        question = 'How' + ' is ' + line.words[bucket['NN']] + ' ' + \
            line.words[bucket['IN']]+' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l24):
        question = 'How' + line.words[bucket['JJ']] + ' ' + \
            line.words[bucket['VBZ']]+' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l25):
        question = 'Which' + ' is ' + \
            line.words[bucket['DT']] + ' ' + line.words[bucket['JJS']
                                                        ]+' ' + line.words[bucket['NNS']] + '?'

    elif all(key in bucket for key in l26):
        question = 'Which' + ' is ' + line.words[bucket['JJR']] + '?'

    elif all(key in bucket for key in l27):
        question = 'Which' + ' is ' + \
            line.words[bucket['DT']] + ' ' + line.words[bucket['JJR']
                                                        ]+' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l28):
        question = 'Which' + '  ' + line.words[bucket['NN']] + ' ' + \
            line.words[bucket['VBZ']]+' ' + line.words[bucket['JJR']] + '?'

    elif all(key in bucket for key in l29):
        question = 'Which' + ' is ' + \
            line.words[bucket['DT']] + ' ' + line.words[bucket['JJR']
                                                        ]+' ' + line.words[bucket['CD']] + '?'

    elif all(key in bucket for key in l30):
        question = 'Who' + ' is ' + line.words[bucket['NNP']] + ' ' + \
            line.words[bucket['POS']]+' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l31):
        question = 'Who' + ' is ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['JJ']]+' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l32):
        question = 'Who' + ' is ' + \
            line.words[bucket['PRP$']] + ' ' + line.words[bucket['NN']] + '?'

    elif all(key in bucket for key in l33):
        question = 'Why' + ' is ' + line.words[bucket['DT']] + ' ' + \
            line.words[bucket['NN']]+' ' + line.words[bucket['JJ']] + '?'

    elif all(key in bucket for key in l34):
        question = 'Why' + ' is ' + \
            line.words[bucket['NNP']] + ' ' + line.words[bucket['VBN']] + '?'

    elif all(key in bucket for key in l35):
        question = 'Why' + ' is ' + \
            line.words[bucket['NN']] + ' ' + line.words[bucket['VBN']] + '?'

    elif all(key in bucket for key in l36):
        question = 'Why' + ' are ' + \
            line.words[bucket['NN']] + ' ' + line.words[bucket['JJ']] + '?'
    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
        question = question.replace(" ’ ", "'s ")
    return question, line
