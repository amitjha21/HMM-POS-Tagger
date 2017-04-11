#--------------------------------------------------------------------------
# Program: hmmlearn3.py
# Author: Amit Jha; Email: amitjha@usc.edu
# Date: 03/07/2017
# Description: hmmlearn.py to learn and create model file
# Input: Single file contaiing tagged training data
# Output: Single hmmmodel.txt with hmm modal parameters
#--------------------------------------------------------------------------

import sys
#0. Declaration
transitionDict = {}
transitionProbDict = {}
tagCountDict = {}
outgoingTagTotalCountDict = {}
wordList = []
emissionProbDict = {}
prevTag = 'Q0'
tagString = ''

#1.Read training file

#if(len(sys.argv)<2):
#    print("Error: No file parameter passed!")
    #exit()
trainingTextFile = 'catalan_corpus_train_tagged.txt' #
#trainingLabelFile = 'train-labels.txt'  #sys.argv[2]

trainFileP = open(trainingTextFile,'r',encoding="utf-8")
for lines in trainFileP:
    wordList.append(lines.split())
trainFileP.close()

# get tags
for line in wordList:
    prevTag = 'Q0'
    tag = ''
    for words in line:               #tag count
        tag = words[-2:]
        if tag in tagCountDict:
            tagCountDict[tag] = tagCountDict[tag] + 1
        else:
            tagCountDict[tag] = 1
        # count total word|TAG
        if words in emissionProbDict.keys():
            emissionProbDict[words] = emissionProbDict[words] + line.count(words)
        else:
            emissionProbDict[words] = line.count(words)

        #get transition counts
        if tag == '' or prevTag == '':
            prevTag = tag
            continue
        tranTagSet = prevTag + '-' + tag
        if tranTagSet in transitionDict:
            transitionDict[tranTagSet] = transitionDict[tranTagSet] + 1
        else:
            transitionDict[tranTagSet] = 1
        # count outgoing tag total count
        if prevTag in outgoingTagTotalCountDict.keys():
            outgoingTagTotalCountDict[prevTag] = outgoingTagTotalCountDict[prevTag] + 1
        else:
            outgoingTagTotalCountDict[prevTag] = 1
        prevTag = tag

#tranTagList = list(transitionDict.keys())
#for i in transitionDict.keys():
#    outTag = i.split('-')[0]
#    if outTag in outgoingTagTotalCountDict.keys():
#        outgoingTagTotalCountDict[outTag] = outgoingTagTotalCountDict[outTag] + transitionDict[i]
#    else:
#        outgoingTagTotalCountDict[outTag] = transitionDict[i]

# transition probability tag WITH smoothing
for i in tagCountDict.keys():
    tagString = tagString + ',' + i
modelFileW = open('hmmmodel.txt','w+')
#write no of states(tags)
modelFileW.write('No. of tags:' + str(len(tagCountDict)) + '\n')
modelFileW.write('Tags:' + tagString.strip(',') + '\n')
modelFileW.write('Outgoing Count:\n')
for i in outgoingTagTotalCountDict.keys():
    modelFileW.write(i+':' + str(outgoingTagTotalCountDict[i])+ '\n')
modelFileW.write('Transition Probability:\n')
for i in transitionDict.keys():
    outTag = i.split('-')[0]
    outTag1 = i.split('-')[1]
    if outgoingTagTotalCountDict[outTag] > 0:
        transitionProbDict[i] = (transitionDict[i] + 1) / (outgoingTagTotalCountDict[outTag] + len(tagCountDict))
        if outTag == 'Q0':
           # ws = 'Begin-' +outTag1+ ':' + str('{:.8f}'.format(transitionProbDict[i])) + '\n'
            t1 = "%f13"%(transitionProbDict[i])
            ws = 'Begin-' + outTag1 + ':' + t1 + '\n'
        else:
            t2 = "%f13" % (transitionProbDict[i])
            #ws = i + ':' + str('{:.8f}'.format(transitionProbDict[i])) + '\n'
            ws = i + ':' + t2 + '\n'
        modelFileW.write(ws)
        ws = ''

l = len(transitionDict)

# Emission Probablity
modelFileW.write('\n\n\nEmission Probability:\n')
for i in emissionProbDict.keys():
    Tag = i[-2:]
    if tagCountDict[Tag] > 0:
        emissionProbDict[i] = emissionProbDict[i] / tagCountDict[Tag]
        t3 = "%f13" % (emissionProbDict[i])
        ws = 'P('+i[0:len(i)-3]+'|'+Tag+'):->' + t3 + '\n'
        modelFileW.write(ws)
#print (l)