import subprocess


class EOL(Exception):
    pass


class Parser:
    def __init__(self, filename, code):
        self.filename = filename
        self.cur = 0
        self.code = code
        self.look_ahead = code[0]

        self.bpm = 120
        self.velocity = 90
        self.instrument = 'Cello'
        self.note_code = ''
        self.note_code_reset_flag = False

        self.middle_midi_list = []

        self.drum_mode = False
        self.instruments = []

    def _match(self, x):
        if self.look_ahead == x:
            self._consume()
        else:
            raise RuntimeError("not match {}".format(x))

    def _match_str(self, xs):
        for x in xs:
            self._match(x)

    def _ignore_ws(self):
        while self.look_ahead in ' \t\n':
            self._consume()

    def _ws(self):
        if self.look_ahead not in ' \t\n':
            raise RuntimeError("not match white space")
        self._ignore_ws()

    def _int(self):
        int_str = ''
        while self.look_ahead in '0123456789':
            int_str += self.look_ahead
            self._consume()
        return int(int_str)

    def _str(self):
        s = ''
        while self.look_ahead.isalpha() or self.look_ahead in "0123456789":
            s += self.look_ahead
            self._consume()
        return s

    def _consume(self):
        self.cur += 1
        if len(self.code) == self.cur:
            raise EOL
        self.look_ahead = self.code[self.cur]

    def process_note_code(self):
        print('note code', self.note_code)
        filename = '{0}-{2}-{1}.mid'.format(self.filename, self.instrument,
                                            len(self.middle_midi_list))
        print("process", self.instrument)
        if '-' in self.instrument:
            subprocess.call(
                'echo \'{code}\' | python3 drum_seq.py \'[{insts}]\' {bpm} {filename} {velocity}'
                .format(code=self.note_code,
                        insts=','.join(['"' + s + '"' for s in self.instruments]),
                        bpm=self.bpm,
                        velocity=self.velocity,
                        filename=filename),
                shell=True)
        else:
            subprocess.call(
                'echo \'{code}\' | python3 chord_bass_seq.py \'{inst}\' {bpm} {filename} {velocity}'
                .format(code=self.note_code,
                        inst=self.instrument,
                        bpm=self.bpm,
                        velocity=self.velocity,
                        filename=filename),
                shell=True)
        self.middle_midi_list.append(filename)
        self.note_code = ''

    def parse(self):
        try:
            while True:
                self._ignore_ws()
                if self.look_ahead == 'b':
                    self._match_str('bpm')
                    self._ignore_ws()
                    self._match('=')
                    self._ignore_ws()
                    self.bpm = self._int()
                    print('bpm', self.bpm)
                    self._ws()
                elif self.look_ahead == 'v':
                    self._match_str('velocity')
                    self._ignore_ws()
                    self._match('=')
                    self._ignore_ws()
                    self.velocity = self._int()
                    print('velocity', self.velocity)
                    self._ws()
                elif self.look_ahead == 'i':
                    if self.note_code != '':
                        self.process_note_code()
                    self._match_str('instrument')
                    self._ignore_ws()
                    self._match('=')
                    self._ignore_ws()
                    if self.drum_mode:
                        self._match('{')
                        self._ignore_ws()
                        instruments = []
                        instruments.append(self._str())
                        self._ignore_ws()
                        while self.look_ahead == ',':
                            self._consume()
                            self._ignore_ws()
                            instruments.append(self._str())
                            self._ignore_ws()
                        self._match('}')
                        self.instruments = instruments
                        self.instrument = '-'.join(instruments)
                        print('instrument detected', self.instrument)
                    else:
                        self.instrument = self._str()
                        print('instrument detected', self.instrument)
                    self._ws()
                elif self.look_ahead == 'd':
                    print()
                    print(self.code[self.cur:])
                    self._match_str('drum')
                    self.drum_mode = True
                    print("drum_mode on")
                elif self.look_ahead == '|':
                    print('note code detect')
                    while self.look_ahead != '\n':
                        self.note_code += self.look_ahead
                        self._consume()
        except EOL:
            print("end")
        if self.note_code != '':
            print('note code', self.note_code)
            self.process_note_code()

        print("stack", self.middle_midi_list)
        subprocess.call('python3 stack_midi.py \'[{0}]\' {1}.mid'.format(
            ','.join(['"' + s + '"' for s in self.middle_midi_list]),
            self.filename),
                        shell=True)


def main(filename):
    with open(filename, 'r') as f:
        code = f.read()
    parser = Parser(filename, code)
    try:
        parser.parse()
    except RuntimeError as e:
        print('"{}"'.format(parser.look_ahead))
        raise e


if __name__ == "__main__":
    import fire
    fire.Fire(main)
