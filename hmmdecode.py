# coding=utf-8
import sys, math, collections, json, io, codecs

# model = {}
# taglist = []
# transitionProb = {}
# emissionProb = {}

with codecs.open("hmmmodel.txt") as modelfile:
    model = eval(json.loads(modelfile.read().decode("utf-8-sig"), encoding="utf-8",))
    modelfile.close()

transitionProb = model["transition"]
emissionProb = model['emission']
taglist = model['tags']
taglist.remove("q0")
# print taglist

def viterbi(observations):
    numobs = len(observations)
    taggedlist = [''] * numobs
    probability = collections.defaultdict(dict)
    backpointer = collections.defaultdict(dict)
    # print observations[0]
    if emissionProb.has_key(observations[0]):
        for tag in emissionProb[observations[0]].keys():
            if emissionProb[observations[0]].has_key(tag):
                probability[0][tag] = (float(transitionProb["q0"][tag])) + (float(emissionProb[observations[0]][tag]))
                backpointer[0][tag] = "q0"
                # print "known " + tag
                # print probability[tag][0]
                # print backpointer[tag][0]
    else:
        for tag in taglist:
            probability[0][tag] = (float(transitionProb["q0"][tag]))
            backpointer[0][tag] = "q0"
            # print "unknown " + tag
            # print probability[tag][0]

    for i in range(1, numobs):
        if emissionProb.has_key(observations[i]):
            for tag in emissionProb[observations[i]].keys():
                tempdict = {}
                for innertag in probability[i-1].keys():
                    tempdict[innertag] = float(probability[i-1][innertag]) + (float(transitionProb[innertag][tag])) + (float(emissionProb[observations[i]][tag]))
                temp = max(tempdict.items(), key=lambda k: k[1])
                backpointer[i][tag] = temp[0]
                probability[i][tag] = temp[1]
        else:
            for tag in taglist:
                tempdict = {}
                for innertag in probability[i-1].keys():
                    tempdict[innertag] = float(probability[i-1][innertag]) + (float(transitionProb[innertag][tag]))
                temp = max(tempdict.items(), key=lambda k: k[1])
                backpointer[i][tag] = temp[0]
                probability[i][tag] = temp[1]

    finaltag = max(probability[numobs-1].items(), key=lambda k:k[1])
    taggedlist[numobs-1] = finaltag[0]
    for j in range(numobs-1,0,-1):
        taggedlist[j-1] = backpointer[j][taggedlist[j]]
    for i in range(0,numobs):
        observations[i] = observations[i] + "/" + taggedlist[i]
    return " ".join(observations)




# print "taglist: " + str(taglist)
# print "transitionProb: " + repr(transitionProb['q0']['PP'])
# with io.open("temp.txt",'r', encoding="utf-8") as tempfile:
#     for line in tempfile:
#         words = line.strip().split()
#         # print words[0]
#         print "EmissionProb: " + repr(emissionProb[words[0]])
#     tempfile.close()
# print repr(emissionProb[''])
# for key in model['emission'].keys():
# for innerkey in model['emission']['NP'].keys():
#     print innerkey
#     innerkey1 = innerkey.encode(encoding="utf-8")
#     print model['emission']['NP'][innerkey]
# with io.open("temp.txt") as tempfile:
#     for line in tempfile:
#         words = line.strip().split()
#         # words[0] = words[0].encode(encoding="utf-8")
#         print repr(model['emission'][words[0]]['NC'])
#     # print eval(repr((model['emission']['NP'])))
#     tempfile.close()
# # print (eval(repr((model['emission']['VA']))))

with io.open("hmmoutput.txt", "w", encoding="utf-8") as outputfile:
    with io.open(sys.argv[1],'r',encoding="utf-8") as testfile:
        for line in testfile:
            # outputfile.write(line)
            words = line.strip().split()
            tagged = viterbi(words)
            # for i in xrange(0,len(words)):
            #     finaltag = tagged.pop(i)
            #     tagged.insert(i, words[i] + "/" + finaltag)
            outputfile.write(tagged + "\n")
        testfile.close()
    outputfile.close()