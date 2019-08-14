import sys
import math
import pretty_midi


class Note:
    def __init__(self, base: str, accidental: str, octave_num: int):
        self.base = base
        self.accidental = accidental
        self.octave_num = octave_num

    def name(self):
        return self.base + self.accidental + str(self.octave_num)

    def __repr__(self):
        return self.name()


class MidiGenerator:
    def __init__(self, instrument_list, bpm, velocity):
        self.dt4 = int((60 * 1000) / bpm)
        self.t = 0
        self.velocity = velocity
        self.instrument_list = instrument_list

        program = 20  #pretty_midi.instrument_name_to_program(instrument)
        self.inst = pretty_midi.Instrument(program=program, is_drum=True)

    def append_rest(self, rest_type):
        dt = self.dt4 * 2**(2 - math.log2(rest_type))
        self.t += dt

    def append_note(self, note_type, index_list):
        dt = self.dt4 * 2**(2 - math.log2(note_type))
        print(index_list, dt)
        for index in index_list:
            note_number = pretty_midi.drum_name_to_note_number(
                self.instrument_list[index])
            note = pretty_midi.Note(velocity=self.velocity,
                                    pitch=note_number,
                                    start=self.t / 1000,
                                    end=(self.t + dt) / 1000)
            self.inst.notes.append(note)
        self.t += dt

    def finish_bar(self):
        left = self.t % (4 * self.dt4)
        if left != 0:
            self.t += left

    def write(self, filename):
        midi = pretty_midi.PrettyMIDI()
        midi.instruments.append(self.inst)
        midi.write(filename)


class EOL(Exception):
    pass


class Parser:
    def __init__(self, midi_gen, code):
        self.cur = 0
        self.midi_gen = midi_gen
        self.code = code
        self.look_ahead = code[0]
        self.index_list = []
        self.index_list_reset_flag = False
        self.last_index = 'c'

    def _match(self, x):
        if self.look_ahead == x:
            self._consume()
        else:
            raise RuntimeError("not match {}".format(x))

    def _consume(self):
        self.cur += 1
        if len(self.code) == self.cur:
            raise EOL
        self.look_ahead = self.code[self.cur]

    def parse(self):
        try:
            while True:
                if self.look_ahead == ';':
                    print('end')
                    return
                elif self.look_ahead == '|':
                    print('finish bar')
                    self.midi_gen.finish_bar()
                    self._consume()
                elif self.look_ahead in (' ', '\t', '\n'):
                    print('ignore')
                    self._consume()
                elif self.look_ahead in "0123456789":
                    print('set index', self.look_ahead)
                    if self.index_list_reset_flag:
                        self.index_list = []
                        self.index_list_reset_flag = False
                    index = int(self.look_ahead)
                    self._consume()
                    self.index_list.append(index)
                    self.last_index = index
                elif self.look_ahead in ".*":
                    print('rest')
                    if self.look_ahead == '.':
                        self.midi_gen.append_rest(16)
                    elif self.look_ahead == '*':
                        self.midi_gen.append_rest(4)
                    self._consume()
                elif self.look_ahead in "ihqox":
                    self.index_list_reset_flag = True
                    if self.look_ahead == 'i':
                        self.midi_gen.append_note(1, self.index_list)
                    elif self.look_ahead == 'h':
                        self.midi_gen.append_note(2, self.index_list)
                    elif self.look_ahead == 'q':
                        self.midi_gen.append_note(4, self.index_list)
                    elif self.look_ahead == 'o':
                        self.midi_gen.append_note(8, self.index_list)
                    elif self.look_ahead == 'x':
                        self.midi_gen.append_note(16, self.index_list)
                    self._consume()
                else:
                    print(self.look_ahead)
                    raise
        except EOL:
            print("end")


def main(instrument_list: str, bpm: int, filename: str, velocity: int):
    midi_gen = MidiGenerator(instrument_list, bpm, velocity)
    parser = Parser(midi_gen, sys.stdin.read())
    parser.parse()
    midi_gen.write(filename)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
