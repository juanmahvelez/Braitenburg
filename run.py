from generate import make_song
from parse_midi import patterns_to_midi_v2

midi_in = './midi/train.mid'
midi_out = './midi/out.mid'
patterns = make_song(midi_in = midi_in, window_size = 64)
patterns_to_midi_v2(patterns, midi_out)
