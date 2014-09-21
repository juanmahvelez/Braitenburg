#!/usr/bin/env python 
import random, parse_midi
song = [[1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1], [0,1,0,1,1,1,0], [1,1,1,1,0,0,0]]

def magic(track, windowSize):
	model = createModel(track, windowSize)
	return model


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
	#print model
	return model

def generate(sequence, model, length, order):
	for i in range(length):
		pattern = sequence[-order:]

		while not model.has_key(tuple(pattern)):
			#print "no ", tuple(pattern)
			pattern = pattern[1:]
		
		chanceZero = model[tuple(pattern)][0]
		chanceOne = model[tuple(pattern)][1]

		rando = chanceZero + chanceOne
		rr = random.randint(1,rando)
		#print rr, "random number"
		newBeat = 1
		if rr<=chanceZero:
			newBeat = 0

		sequence.append(newBeat)
	#print sequence
	return sequence

def make_song():
	midi_in = "./midi/train.mid"

	song = parse_midi.midi_to_patterns(midi_in)

	result = {}
	for track in song:
		print "workin on " , track 
		trax = [int(i) for i in song[track]]
		sequence = generate([1,0,0,0], magic(trax,256), 2000, 256)
		sequence = [float(j) for j in sequence]
		result[track] = sequence 
	print result
	return result
make_song()

