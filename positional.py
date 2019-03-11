# BismiAllahirRahmaanirRaheem
import re, os, time
from pprint import pprint

def fetchCollection():
    terms = []
    docId = {}
    index = {}
    stats = {}
    path = 'F:\hesh.@\\6th semester\I.R\Assignment-1\ShortStories'
    collecCount = 0
    tokenCount = 0

    for filename in os.listdir(path):
        size = 0
        collecFile = open(os.path.join('F:\hesh.@\\6th semester\I.R\Assignment-1\ShortStories',filename), 'r')
        story = collecFile.readline()
        author = collecFile.readline()
        author = author.replace('by','')
        docId.setdefault(story,filename.strip('.txt'))
        # print(story, author)
        tempp = 0
        for i, line in enumerate(collecFile):
            if i > 0:
                line = filter(None, re.split("[, \-!?:_]+", line))

                for p,word in enumerate(line):
                    p =tempp+1
                    collecCount += 1
                    # re.sub(r'[^\w\s]', '', s)
                    word = re.findall(r'[\w]+', word.casefold())
                    if word:
                        tokenCount += 1
                        if word[0]:
                            size += 1
                            index.setdefault(word[0], {}).setdefault(docId[story], []).append(p)
                            tempp = p

        stats.setdefault(docId[story], size)

    return dict(sorted(index.items())), collecCount, stats


if __name__ == '__main__':

    print("\n------------Ad-Hoc Retrieval via Positional Index-----------\n\n ***Statistics about Collection***")

    start = time.clock()
    index, T, stats = fetchCollection()
    print("Index established in: %.3f seconds" % (time.clock() - start))
    out = open("dict.pickle", "wb")
    pickle.dump(index, out)
    out.close()
    print('Tokens in Collection (T):', T)
    print('Applying HEAP\'s Law with k = 34 and b = 0.49,\nwe get M ~ ', int(34.0 * (T ** 0.49)))
    print('Actual terms in Collection (M):', len(index.keys()))
    # print(stats)
    print('Smallest document w.r.t No. of tokens: ', min(stats, key=stats.get),
          '\nLargest document w.r.t No. of tokens: ', max(stats, key=stats.get),
          '\nAverage No. of tokens per Document', sum(stats.values()) / 50)
    print('\n(Kindly abide by following query format)\n *Supported Query format:\n - Proximity '
          'Query:\n   x y /k\n - Phrase Query:\n   x y\n   x y z ')
    answer = []
    choice = ''
    while choice != 'exit':

        choice = input('Enter 1 for Proximity Query Or 2 for Phrase Query Or exit to terminate>>')
        # q = 'noise down /2'
        if choice != 'exit':
            q = input('Enter Query>>')
            qToken = []
            answer = []
            qList = list(filter(None, re.split("[, \!?:_]+", q.casefold())))

            for q in qList:
                q = re.findall(r'[a-zA-Z0-9]+', q)
                if q: qToken.append(q[0])

            # print(qToken)
            try:

                if int(choice) == 1:
                    start = time.clock()
                    if len(qToken) == 3:
                        docs = (sorted(set(index[qToken[0]]) & set(index[qToken[1]]), key=int))
                        # print(docs)

                        for doc in docs:
                            q1 = index[qToken[0]][doc]
                            q2 = index[qToken[1]][doc]
                            for first in q1:
                                for second in q2:
                                    if first == second - (int(qToken[2]) + 1):
                                        if doc not in answer: answer.append(doc)

                    else: print('Please abide by the stated query format')

                elif int(choice) == 2:

                    if len(qToken) == 2:
                        start = time.clock()
                        docs = (sorted(set(index[qToken[0]]) & set(index[qToken[1]]), key=int))
                        # print(docs)

                        for doc in docs:
                            q1 = index[qToken[0]][doc]
                            q2 = index[qToken[1]][doc]
                            for first in q1:
                                for second in q2:
                                    if first == second - 1:
                                        if doc not in answer: answer.append(doc)

                    elif len(qToken) == 3:
                        start = time.clock()
                        docs = (set(index[qToken[0]]) & set(index[qToken[1]]))
                        docs = (sorted(docs & set(index[qToken[2]]), key=int))

                        for doc in docs:
                            q1 = index[qToken[0]][doc]
                            q2 = index[qToken[1]][doc]
                            q3 = index[qToken[2]][doc]
                            for first in q1:
                                for second in q2:
                                    for third in q3:
                                        if first == second - 1 and second == third -1:
                                            if doc not in answer: answer.append(doc)


                    else:
                        print('Please abide by the stated query format')
            except KeyError:
                print('Key Error raised')

    print(len(answer), ' Docs. retrieved in %.2f milliseconds' % ((time.clock() - start) * 1000))
    print('Matched documents are: ', answer)

