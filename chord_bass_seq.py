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
    def __init__(self, instrument, bpm, velocity):
        self.dt4 = int((60 * 1000) / bpm)
        self.t = 0
        self.velocity = velocity

        program = pretty_midi.instrument_name_to_program(instrument)
        self.inst = pretty_midi.Instrument(program=program)

    def append_rest(self, rest_type):
        dt = self.dt4 * 2**(2 - math.log2(rest_type))
        self.t += dt

    def append_note(self, note_type, note_list):
        dt = self.dt4 * 2**(2 - math.log2(note_type))
        print(note_list, dt)
        for note in note_list:
            note_number = pretty_midi.note_name_to_number(note.name())
            note = pretty_midi.Note(velocity=self.velocity,
                                    pitch=note_number,
                                    start=self.t/1000,
                                    end=(self.t + dt)/1000)
            self.inst.notes.append(note)
        self.t += dt

    def finish_bar(self):
        left = self.t % (4*self.dt4)
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
        self.note_list = []
        self.note_list_reset_flag = False
        self.last_note_base = 'c'
        self.last_octave = 3

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
                if self.look_ahead == '|':
                    print('finish bar')
                    self.midi_gen.finish_bar()
                    self._consume()
                elif self.look_ahead in (' ', '\t', '\n'):
                    print('ignore')
                    self._consume()
                elif self.look_ahead in "abcdefg":
                    print('set note', self.look_ahead)
                    if self.note_list_reset_flag:
                        self.note_list = []
                        self.note_list_reset_flag = False
                    note_base = self.look_ahead
                    self._consume()
                    if self.look_ahead in "!#":
                        accidental = self.look_ahead
                        self._consume()
                    else:
                        accidental = ''
                    if self.look_ahead in "0123456789":
                        octave = int(self.look_ahead)
                        self._consume()
                    else:
                        octave = int(self.last_octave)
                        if (ord(self.last_note_base) - ord(note_base)) > 0:
                            print("+1 octave")
                            octave += 1
                    self.note_list.append(
                        Note(note_base.capitalize(), accidental, octave))
                    self.last_note_base = note_base
                    self.last_octave = octave
                elif self.look_ahead in ".*":
                    print('rest')
                    if self.look_ahead == '.':
                        self.midi_gen.append_rest(16)
                    elif self.look_ahead == '*':
                        self.midi_gen.append_rest(4)
                    self._consume()
                elif self.look_ahead in "ihqox":
                    self.note_list_reset_flag = True
                    if self.look_ahead == 'i':
                        self.midi_gen.append_note(1, self.note_list)
                    elif self.look_ahead == 'h':
                        self.midi_gen.append_note(2, self.note_list)
                    elif self.look_ahead == 'q':
                        self.midi_gen.append_note(4, self.note_list)
                    elif self.look_ahead == 'o':
                        self.midi_gen.append_note(8, self.note_list)
                    elif self.look_ahead == 'x':
                        self.midi_gen.append_note(16, self.note_list)
                    self._consume()
                else:
                    raise RuntimeError("invalid charactor: ", self.look_ahead)
        except EOL:
            print("end")


def main(instrument: str, bpm: int, filename: str, velocity: int):
    midi_gen = MidiGenerator(instrument, bpm, velocity)
    parser = Parser(midi_gen, sys.stdin.read())
    parser.parse()
    midi_gen.write(filename)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
