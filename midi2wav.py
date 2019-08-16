import pretty_midi
from scipy.io import wavfile


def main(midi_filename, wav_filename):
    midi = pretty_midi.PrettyMIDI(midi_filename)
    audio = midi.fluidsynth()
    wavfile.write(wav_filename, 44100, audio)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
