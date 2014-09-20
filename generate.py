#!/usr/bin/env python 
import random, parse_midi
song = [[1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1], [0,1,0,1,1,1,0], [1,1,1,1,0,0,0]]

def magic(song, windowSize):
	for track in song:
		model = createModel(track, windowSize)
		return model
	return 


def createModel(track, windowSizeX):
	model = {(0,1):(1,1), (1,0):(1,1), (0,0):(1,1), (1,1):(1,1)}

	for windowSize in range(3,windowSizeX + 1):
		#print "window Size = ", windowSize
		for i in range(len(track)-windowSize+1):
			pattern = tuple(track[i:(i+windowSize)])
			nMinusOnePattern = tuple(track[i:(i+windowSize-1)])
			nextBeat = track[i+windowSize-1]


			if nMinusOnePattern in model:
				currentVal = model[nMinusOnePattern]
				if nextBeat == 1:
					model[nMinusOnePattern] = (currentVal[0], currentVal[1] + 1)
				else:
					model[nMinusOnePattern] = (currentVal[0] + 1, currentVal[1])
			else:
				if nextBeat == 1:
					value = (1,2)
				else:
					value = (2,1)
				model[nMinusOnePattern] = value
	print model
	return model

def generate(sequence, model, length, order):
	for i in range(length):
		pattern = sequence[-order:]

		while not model.has_key(tuple(pattern)):
			print "no ", tuple(pattern)
			pattern = pattern[1:]
			raw_input()
		
		chanceZero = model[tuple(pattern)][0]
		chanceOne = model[tuple(pattern)][1]

		rando = chanceZero + chanceOne
		rr = random.randint(1,rando)
		print rr, "random number"
		newBeat = 1
		if rr<=chanceZero:
			newBeat = 0

		print "found pattern ", tuple(pattern), model[tuple(pattern)]
		sequence.append(newBeat)
		print "new sequence", sequence



generate([1,0,1,0,1], magic(song,4), 10, 4)

