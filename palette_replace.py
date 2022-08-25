#!/usr/bin/env python3

import argparse
from pathlib import Path
import jstyleson
import logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--palette", required=True, type=str)
    parser.add_argument("--header", required=False, type=str)
    parser.add_argument("--footer", required=False, type=str)
    parser.add_argument("--verbose",
                        required=False,
                        type=bool,
                        action="set_true",
                        default=False)
    args = parser.parse_args()
    return args


def set_args(template,
             output,
             palette,
             header=None,
             footer=None,
             verbose=False):
    return argparse.Namespace(template=template,
                              output=output,
                              palette=palette,
                              header=header,
                              footer=footer,
                              verbose=verbose)


def read_in(filepath):
    logging.info(f"Reading template \"{filepath}\"")
    return Path(filepath).read_text()


def read_palette(filepath):
    logging.info(f"Reading palette \"{filepath}\"")
    with Path(filepath).open() as f:
        return jstyleson.load(f)


def write_out(filepath, text):
    logging.info(f"Writing \"{filepath}\"")
    return Path(filepath).write_text(text)


def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    logging.info("=" * 100)
    logging.info("")
    template = read_in(args.template)
    palette = read_palette(args.palette)
    output = template.format(**palette)
    assert not "{" in output
    assert not "}" in output

    if args.header is not None:
        logging.info("Header defined")
        header = read_in(args.header)
        output = header + output

    if args.footer is not None:
        logging.info("Footer defined")
        footer = read_in(args.footer)
        output = output + footer

    write_out(args.output, output)
    logging.info("")


if __name__ == "__main__":
    args = parse_args()
    main(args)
