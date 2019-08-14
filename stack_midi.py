import pretty_midi


def main(src_filename_list, dst_filename):
    dst_midi = pretty_midi.PrettyMIDI()
    for filename in src_filename_list:
        src_midi = pretty_midi.PrettyMIDI(filename)
        dst_midi.instruments.extend(src_midi.instruments)
    dst_midi.write(dst_filename)


if __name__ == '__main__':
    import fire
    fire.Fire(main)
