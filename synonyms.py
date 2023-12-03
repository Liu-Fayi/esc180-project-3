'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    print("cosine_similarity")
    dp = 0
    for key in vec1:
        if key in vec2:
            dp += vec1[key] * vec2[key]
    return dp / (norm(vec1) * norm(vec2))


def build_semantic_descriptors(sentences):
    print("build_semantic_descriptors")
    # if sentences == [['']]:
    #     return {}
    d = {}
    for sentence in sentences:
        temp = {}
        for word in sentence:
            if word != "":
                if word not in d:
                    d[word] = {}
                if word not in temp:
                    temp[word] = 0
                temp[word] += 1
        # try:
        #     temp.pop("")
        # except:
        #     pass
        for word in sentence:
            if word != "":
                t = temp.copy()
                t.pop(word)
                for key in t:
                    if key not in d[word]:
                        d[word][key] = 0
                    d[word][key] += t[key]
    # print(d)
    return d


def build_semantic_descriptors_from_files(filenames):
    print("build_semantic_descriptors_from_files")
    files = [None] * len(filenames)
    texts = [None] * len(filenames)
    sentences = []
    for i in range(len(filenames)):
        files[i] = open(filenames[i], "r", encoding="utf-8")
        texts[i] = files[i].read()
        files[i].close()
        texts[i] = texts[i].lower()
        texts[i] = texts[i].replace("\n", " ")
        texts[i] = texts[i].replace("!", ".")
        texts[i] = texts[i].replace("?", ".")
        texts[i] = texts[i].replace(",", "")
        texts[i] = texts[i].replace(";", "")
        texts[i] = texts[i].replace(":", "")
        texts[i] = texts[i].replace("-", "")
        texts[i] = texts[i].replace("'", "")
        texts[i] = texts[i].replace("(", "")
        texts[i] = texts[i].replace(")", "")
        texts[i] = texts[i].replace('"', "")
        texts[i] = texts[i].replace("\ufeff", "")
        sentences.append(texts[i].split("."))
    for i in range(len(sentences)):
        sentences[i] = [x.split(" ") for x in sentences[i]]

    d = {}
    for i in sentences:
        temp = build_semantic_descriptors(i)
        for key in temp:
            if key not in d:
                d[key] = {}
            for key2 in temp[key]:
                if key2 not in d[key]:
                    d[key][key2] = 0
                d[key][key2] += temp[key][key2]

    return d


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    print("most_similar_word")
    max = -1
    choice = 0
    for i in range(len(choices)):
        try:
            t = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
        except:
            t = -1
        if t > max:
            max = t
            choice = i
    return choices[choice]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    print("run_similarity_test")
    open_file = open(filename, "r", encoding="utf-8")
    text = open_file.read()
    open_file.close()
    text = text.split("\n")
    for i in range(len(text)):
        text[i] = text[i].split(" ")
    if text[-1] == ['']:
        text.pop()
    correct = 0
    total = len(text)
    for i in text:
        if i[1] == most_similar_word(i[0], i[2:], semantic_descriptors, similarity_fn):
            correct += 1

    return correct / total


if __name__ == "__main__":
    slist = [['this', 'is', 'file', 'one'],
                ['this', 'is', 'file', 'two'],
                ['file', 'two', 'has', 'two', 'sentences'],
                ['this', 'is', 'file', 'three'],
                ['file', 'three', 'has', 'three', 'sentences'],
                ['this', 'is', 'the', 'third', 'sentence']]
    vecs = build_semantic_descriptors(slist)
    expected = {'this':1, 'is':1, 'the':1, 'sentence':1}
    if '' in vecs['third']: del vecs['third']['']
    print(vecs['third'])
    # sem_descriptors = build_semantic_descriptors_from_files(["2600-0.txt", "pg7178.txt"])
    # res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    # print(res, "of the guesses were correct")
    # print(build_semantic_descriptors([["i","am","a","sick","man"], ["i","am","a","spiteful","man"]]))
