#!/usr/bin/env python
import argparse
import logging
import sys

from .__init__ import __version__
from .samplot import add_plot
from .samplot_vcf import add_vcf


def main(args=None):
    # logs all messages with a level above INFO in sys.stderr
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(module)s - %(levelname)s: %(message)s")

    # get command line input if there are no other args
    if args is None:
        args = sys.argv[1:]

    # create parsers for
    parser = argparse.ArgumentParser(
        prog="samplot", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # define arguments
    parser.add_argument(
        "-v",
        "--version",
        help="Installed version",
        action="version",
        version="%(prog)s " + str(__version__),
    )
    sub = parser.add_subparsers(title="[sub-commands]", dest="command")
    sub.required = True

    add_plot(sub)   # defines arguments to plot
    add_vcf(sub)    # defines arguments for samplot's vcf plotter

    # parse
    args,extra_args = parser.parse_known_args(args)
    args.func(parser, args, extra_args)


if __name__ == "__main__":
    sys.exit(main() or 0)
