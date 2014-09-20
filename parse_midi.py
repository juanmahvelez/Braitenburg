import csv
import os
from collections import defaultdict
import numpy as np
from math import ceil

def midi_to_patterns(midi_in, csv_out = 'drums.csv'):
  os.system(" ".join(["midicsv", midi_in, ">", csv_out]))

  ticks_per_32nd_note = 12

  reader = csv.reader(open(csv_out, 'r'), delimiter = ',')
  tracks = defaultdict(list)
  patterns = {}
  max_tick = -1
 
  for line in reader:
    tick = int(line[1])
    event = line[2].strip()
    if event != 'Note_on_c':
      continue
    id = int(line[4].strip()) 
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

def patterns_to_midi(patterns):
  header_lines = [[0, 0, 'Header', 0, 1, 96
1, 0, Start_track
1, 0, Title_t, "MIDI Drums\000"
1, 0, Time_signature, 4, 2, 36, 8
1, 0, Time_signature, 4, 2, 36, 8


midi_in = "~/Downloads/MIDI_Drums_q16_16t.mid"
csv_out = 'drums.csv'

midi_to_tracks(midi_in)
