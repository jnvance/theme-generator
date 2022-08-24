#!/usr/bin/env python3

import argparse
from pathlib import Path
import jstyleson


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--palette", required=True, type=str)
    parser.add_argument("--header", required=False, type=str)
    parser.add_argument("--footer", required=False, type=str)
    args = parser.parse_args()
    return args


def read_in(filepath):
    return Path(filepath).read_text()


def read_palette(filepath):
    with Path(filepath).open() as f:
        return jstyleson.load(f)


def write_out(filepath, text):
    return Path(filepath).write_text(text)


if __name__ == "__main__":
    args = parse_args()

    text_in = read_in(args.input)
    palette = read_palette(args.palette)
    text_out = text_in.format(**palette)
    assert not "{" in text_out
    assert not "}" in text_out

    if args.header is not None:
        header = read_in(args.header)
        text_out = header + text_out

    if args.footer is not None:
        footer = read_in(args.footer)
        text_out = text_out + footer

    write_out(args.output, text_out)
