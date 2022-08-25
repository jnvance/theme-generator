#!/usr/bin/env python3

import argparse
import palette_replace as pr
from pathlib import Path

prefix = "jnv_theme_generator_"

##########################################################################
### Define generator functions here with prefix


def jnv_theme_generator_qtcreator():
    pass


def jnv_theme_generator_guake():

    def gen_guake(theme="artemis", style="dark"):
        src = source_directory()
        template_dir = src.joinpath("templates").joinpath("guake")

        args = pr.set_args(
            template=template_dir.joinpath(f"{theme}.sh.in"),
            header=template_dir.joinpath("guake-header.sh.in"),
            footer=template_dir.joinpath("guake-footer.sh.in"),
            palette=src.joinpath("palettes").joinpath(f"{theme}-{style}.json"),
            output=src.joinpath("output").joinpath("guake").joinpath(
                f"{theme}-{style}.sh"),
            verbose=True)
        pr.main(args)

    gen_guake(style="dark")
    gen_guake(style="light")


##########################################################################

all_generators = [f for f in dir() if f.startswith(prefix)]
choices = [f.split(prefix)[-1] for f in all_generators]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("app", nargs="?", choices=choices)
    args = parser.parse_args()
    return args


def source_directory():
    return Path(__file__).parents[0]


def generate_one(name):
    globals()[name]()


def generate_all():
    for name in all_generators:
        generate_one(name)


def generate_from_args(args):
    if args.app is None:
        generate_all()
    else:
        generate_one(prefix + args.app)


if __name__ == "__main__":
    args = parse_args()
    generate_from_args(args)
    # jnv_theme_generator_guake()
