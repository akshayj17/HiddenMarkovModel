import sys, math, collections, json, codecs
import io

transition_prob = collections.defaultdict(dict)
emission_prob = collections.defaultdict(dict)
transition_prob_log = collections.defaultdict(dict)
emission_prob_log = collections.defaultdict(dict)
model = {}
divide_transition = {}
divide_emission ={}
# d['dict1']['innerkey'] = 'value'
# print dict(d)
# print d['dict1'].get('innerkey',0)

# with open("temp.txt", "w") as tempfile:
with codecs.open(sys.argv[1], "r", encoding="utf-8") as trainFile:
    for line in trainFile:
        tokens = line.strip().split()
        prev = "q0"
        # print tokens
        for token in tokens:
            current = token[-2:]
            current_token = token[0:len(token)-3]
            transition_prob[prev][current] = transition_prob[prev].get(current, 0.0) + 1.0
            divide_transition[prev] = divide_transition.get(prev, 0.0) + 1.0
            emission_prob[current_token][current] = emission_prob[current_token].get(current, 0.0) + 1.0
            divide_emission[current] = divide_emission.get(current, 0.0) + 1.0
            prev = current
            # print current
            # prev = current
        # tempfile.write(prev + "\n")
    trainFile.close()
    # tempfile.close()
with io.open("hmmmodel.txt","w",encoding='utf-8') as modelFile:
    # modelFile.write("Transition probabilities: " + "\n")# + repr(divide_transition))
    for key in transition_prob.keys():
        for innerkey in transition_prob.keys():
            transition_prob_log[key][innerkey] = repr(math.log((transition_prob[key].get(innerkey,1.0) + 1.0)/(divide_transition[key] + len(list(transition_prob.keys())))))
        # modelFile.write(key + ": " + repr(transition_prob_log[key]) + "\n")
    # modelFile.write("Emission probabilities: " + "\n")# + repr(divide_emission))
    # json.dump(transition_prob_log, modelFile)
    for key in emission_prob.keys():
        for innerkey in emission_prob[key]:
            emission_prob_log[key][innerkey] = repr(math.log(emission_prob[key][innerkey]/(divide_emission[innerkey])))
        # modelFile.write(key + ": " + repr(emission_prob_log[key]) + "\n")
        # json.dump(emission_prob_log, modelFile)
#     print key + ": " + str()
#     json.dump(emission_prob_log, modelFile)
# print dict(transition_prob)
    model['transition'] = dict(transition_prob_log)
    model['emission'] = dict(emission_prob_log)
    model['tags'] = list(transition_prob.keys())
    modelFile.write(json.dumps(unicode(repr(model), 'unicode-escape'), ensure_ascii=False))
    # modelFile.write(json.dumps(unicode(repr(model),'utf-8'), ensure_ascii=False))
    modelFile.close()


# print model['tags']
# with open("hmmmodel.txt", "w") as modeltext:
#     modeltext.write(repr(model))
#     modeltext.close()
