1) Download MIDICSV Library http://www.fourmilab.ch/webtools/midicsv/#Download


2) "Make" MIDICSV


3) Run run.py specifying:

midi_in => Your training MIDI data. It has to have three tracks corresponding to Kick, Snare and HiHats with these track names. You can dive in the code to change the track names if you like. 

  MIDI Track "36" => KICK
  
  MIDI Track "38" => SNARE
  
  MIDI Track "42" => HIHAT


midi_out => MIDI out file (could be anything)


window_size => The sliding window size when building the probabilistic model



midi_in = './midi/train.mid'
midi_out = './midi/out.mid'
patterns = make_song(midi_in = midi_in, window_size = 64)
patterns_to_midi_v2(patterns, midi_out)
