# BismiAllahirRahmaanirRaheem
import re, os, time,pickle

def fetchCollection():
    stopWords = ['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no']
    terms = []
    docId = {}
    index = {}
    stats = {}
    path = 'ShortStories'
    tokenCount = 0
    collecCount = 0

    for filename in os.listdir(path):
        collecFile = open(os.path.join('ShortStories',filename), 'r')
        story = collecFile.readline()
        author = collecFile.readline()
        author = author.replace('by','')
        docId.setdefault(story,filename.strip('.txt'))
        # print(story, author)
        tempTerms = []
        for i, line in enumerate(collecFile):
            if i > 0:
                line = filter(None, re.split("[, \-!?:_]+", line))
                for word in line:
                    collecCount += 1
                    word = re.findall(r'[\w]+', word.casefold())
                    if word and word[0] not in stopWords:
                        tokenCount += 1
                        terms.append(word[0])
                        if word[0] not in tempTerms:
                            tempTerms.append(word[0])

                            index.setdefault(word[0], []).append(docId[story])

        stats.setdefault(docId[story], len(tempTerms))

    index = dict(sorted(index.items()))
    return index,collecCount,stats


if __name__ == '__main__':


    print("\n------------Ad-Hoc Retrieval via Inverted Index-----------\n\n ***Statistics about Collection***")

    if not os.path.exists('inverted.pickle'):
        start = time.clock()
        index, T, stats = fetchCollection()
        print("Index established from collection in: %.3f seconds"%(time.clock()-start))
        # writing dictionary to a file
        out = open("inverted.pickle", "wb")
        pickle.dump(index, out)
        out.close()
        print('Tokens in Collection (T):', T)
        print('Applying HEAP\'s Law with k = 34 and b = 0.49,\nwe get M ~ ', int(34.0 * (T ** 0.49)))
        print('Actual terms in Collection (M):', len(index.keys()))
        print('Smallest document w.r.t No. of terms: ', min(stats, key=stats.get),
              '\nLargest document w.r.t No. of terms: ', max(stats, key=stats.get),
              '\nAverage No. of terms per Document', sum(stats.values()) / 50)

    else:
        start = time.clock()
        fetch = open("inverted.pickle", "rb")
        index = pickle.load(fetch)
        print("Index loaded from index dump file in: %.3f seconds" % (time.clock() - start))

    print('\nEnter your Query term: (Kindly abide by following query format)\n *Supported Query format:\n - x\n - x OR y\n '
          '- x AND y\n - x OR y OR z\n - x OR y AND z\n - x AND y OR z\n - x AND y AND z\n(exit to end program)')

    q = ''
    while q != 'exit':
        q = input('>>')
        if q == 'exit': break
        qToken = []
        answer = []
        qList = list(filter(None, re.split("[, \!?:_]+", q.casefold())))

        for q in qList:
            q = re.findall(r'[\w]+', q)
            if q: qToken.append(q[0])

        try:
            if len(qToken) == 1:
                answer = index[qToken[0]]
            elif len(qToken) == 3:
                start = time.clock()
                for i, q in enumerate(qToken):
                    if q == 'and':
                        answer = set(index[qToken[i - 1]]) & set(index[qToken[i + 1]])

                for i, q in enumerate(qToken):
                    if q == 'or':
                        answer = set(index[qToken[i - 1]]) | set(index[qToken[i + 1]])

            elif len(qToken) == 5 and 'not' not in qToken:
                start = time.clock()
                j = 0
                if 'and' not in qToken:
                    for i, q in enumerate(qToken):
                        if q == 'or':
                            ored = set(index[qToken[i - 1]]) | set(index[qToken[i + 1]])
                            j = i
                            # print((ored))
                            break

                    for i, q in enumerate(qToken):
                        if i > j and q == 'or':
                            answer = ored | set(index[qToken[i + 1]])
                            # print((ored))

                elif 'or' not in qToken:
                    for i, q in enumerate(qToken):
                        if q == 'and':
                            anded = set(index[qToken[i - 1]]) & set(index[qToken[i + 1]])
                            j = i
                            # print(anded)
                            break

                    for i, q in enumerate(qToken):
                        if i > j and q == 'and':
                            answer = anded & set(index[qToken[i + 1]])
                            # print(anded)
                else:
                    for i, q in enumerate(qToken):
                        if q == 'and':
                            anded = set(index[qToken[i - 1]]) & set(index[qToken[i + 1]])
                            # print(anded)

                    for i, q in enumerate(qToken):
                        if q == 'or':
                            if q == qToken[-2]:
                                answer = anded | set(index[qToken[i + 1]])
                                # print(ored)
                            else:
                                answer = set(index[qToken[i - 1]]) | anded
                                # print(ored)
            else:
                print("Make sure to abide by allowed query format")

        except KeyError:
            print("term doesen't exist")

        print(len(answer),' Docs. retrieved in %.2f milliseconds'% ((time.clock()-start)*1000))
        print('Matched documents are: ',sorted(answer, key=int))
