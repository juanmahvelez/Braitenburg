import csv
import os
from collections import defaultdict
import numpy as np
from math import ceil

from midiutil.MidiFile import MIDIFile

NOTE_ON = 'Note_on_c'
NOTE_OFF = 'Note_off_c'

ticks_per_32nd_note = 12
velocity_thresh = {
  36: 32, # KICK
  38: 32, # SNARE
  42: 32  # HIHAT
}

def midi_to_patterns(midi_in, csv_out = 'drums.csv'):
  os.system(" ".join(["midicsv", midi_in, ">", csv_out]))

  reader = csv.reader(open(csv_out, 'r'), delimiter = ',')
  tracks = defaultdict(list)
  patterns = {}
  max_tick = -1
 
  for line in reader:
    tick = int(line[1])
    event = line[2].strip()
    if event != NOTE_ON:
      continue
    id = int(line[4].strip()) 
    velocity = int(line[5].strip())
    if velocity < velocity_thresh[id]:
      continue
    tracks[id].append(tick)
    if tick > max_tick:
      max_tick = tick
    print (tick, event, id)
   
  track_len = int(ceil(max_tick / ticks_per_32nd_note))
  if track_len % 2 != 0:
    track_len += 1

  for id, track in tracks.items():
    pattern = np.zeros(track_len)
    pattern[(np.array(track) / ticks_per_32nd_note) - 1] = 1
    patterns[id] = pattern

  print [ pattern.tolist() for id, pattern in patterns.items() ]
  print track_len
  return patterns

def patterns_to_midi(patterns, midi_out, csv_out = 'drums.csv'):
  csv_lines = []
  midi_track = 1
  midi_channel = 0
  velocity = 60

  for id, pattern in patterns.items():
    onsets = np.array([ i for i in range(len(pattern)) if pattern[i] == 1 ])
    ticks = onsets * ticks_per_32nd_note
    for tick in ticks:
      csv_lines.append([midi_track, tick, NOTE_ON, midi_channel, id, velocity])
      # Only 32nd notes
      csv_lines.append([midi_track, tick + ticks_per_32nd_note, NOTE_OFF, midi_channel, id, 64])

  with open(csv_out, 'w') as f:
    writer = csv.writer(f)
    csv_lines.sort(key = lambda x: x[1])
    writer.writerows(csv_lines)

def patterns_to_midi_v2(patterns, midi_out):
  num_tracks = len(patterns)
  midi = MIDIFile(num_tracks)
  tempo = 120
  duration = 1

  # track, time, name
  midi.addTrackName(0, 0, "Track0")
  # track, time, tempo
  midi.addTempo(0, 0, tempo)

  for pattern_id, pattern in patterns.items():
    onsets = np.array([ i for i in range(len(pattern)) if pattern[i] == 1 ])
    
    for onset in onsets:
      midi.addNote(0, 0, pattern_id, onset, duration, 127)

  with open(midi_out, 'wb') as f:
    midi.writeFile(f)

"""
midi_in = "~/Downloads/MIDI_Drums_q16_16t.mid"
midi_out = 'drums.mid'
csv_out = 'drums.csv'

patterns = midi_to_patterns(midi_in)

patterns_to_midi_v2(patterns, midi_out)
"""

#os.system('cat header.csv drums.csv > drums2.csv')
#os.system('csvmidi drums2.csv drums.mid')
