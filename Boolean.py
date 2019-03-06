# BismiAllahirRahmaanirRaheem
import re, os

def fetchCollection():
    stopWords = ['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no']
    terms = []
    docId = {}
    index = {}

    path = 'F:\hesh.@\\6th semester\I.R\Assignment-1\ShortStories'
    tokenCount = 0
    collecCount = 0

    for filename in os.listdir(path):
        collecFile = open(os.path.join('F:\hesh.@\\6th semester\I.R\Assignment-1\ShortStories',filename), 'r')
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
                    # re.sub(r'[^\w\s]', '', s)
                    word = re.findall(r'[\w]+', word.casefold())
                    if word and word[0] not in stopWords:

                        tokenCount += 1

                        terms.append(word[0])
                        if word[0] not in tempTerms:
                            tempTerms.append(word[0])
                            index.setdefault(word[0], []).append(docId[story])

    print('collec:',collecCount,'terms:',tokenCount)
    # story = 'A Blunder\n'
    index = dict(sorted(index.items()))
    print((index.keys()))
    return index

if __name__ == '__main__':

    index = fetchCollection()
    q = 'breakfast AND love'

    q = " NOT 'Breakfast' OR -love-this:' OR _(Hamza)?"
    qList = []
    qList = filter(None, re.split("[, \!?:_]+", q.casefold()))
    for query in qList:
        query = re.findall(r'[\w]+', query.casefold())
        if query:
            print(query[0])
    # print(qList)



