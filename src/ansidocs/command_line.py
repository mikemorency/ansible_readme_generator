import ansidocs.main as ansidocs
import argparse
from os import path
import logging


logger = logging.getLogger(__name__)


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', dest="verbose", action='count', default=0,
                        help="Increase program verbosity, use multiple 'v' for more logging")
    parser.add_argument('--quiet', '-q', dest="quiet", action='store_true',
                        help="Only display errors")

    parser.add_argument("-c", "--config-dir", dest="config_dir",
                        help="Path to the config dir",
                        default=path.join(path.expanduser('~'), '.ansidocs'))

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    gen_parser = subparsers.add_parser("generate", aliases=["gen"], help="Generate or update an existing readme")
    gen_parser.add_argument("-d", "--directory", dest="directory", default=".",
                            help="Directory where readme should be generated")
    gen_parser.add_argument("-l", "--layout", dest="force_layout", required=False,
                            help="Force a layout for the project specified. Default is to let the program auto " +
                            "determine the layout")

    test_parser = subparsers.add_parser("test", help="Test if the existing readme matches the expected readme")

    conf_parser = subparsers.add_parser("config", help="Create or refresh your config directory")
    conf_parser.add_argument("-r", "--refresh-configs", dest="refresh_configs",
                             help="If flag is set, config dir will be removed and recreated with defaults",
                             action='store_true')

    gen_parser.set_defaults(func=gen)
    conf_parser.set_defaults(func=conf)
    test_parser.set_defaults(func=test)

    return parser.parse_args()


def determine_log_level(verbose: int, starting_level: str = "WARNING"):
    # https://docs.python.org/3/library/logging.html#levels
    verbose_level_int = verbose * 10
    calculated_level = logging.getLevelName(starting_level) - verbose_level_int
    if calculated_level < 10:
        calculated_level = 10   # this is the minimum we support, debug
    return logging.getLevelName(calculated_level)


def main():
    args = parseArgs()
    if args.quiet:
        # override any other logging configs
        logging.basicConfig(level=logging.ERROR)
    args.func(args)


def gen(args):
    logging.basicConfig(level=determine_log_level(args.verbose))
    ansidocs.generate(
        directory=args.directory,
        config_dir=args.config_dir,
        force_layout=args.force_layout
    )


def conf(args):
    logging.basicConfig(level=determine_log_level(args.verbose, starting_level="INFO"))
    ansidocs.init_config_dir(
        config_dir=args.config_dir,
        refresh_configs=args.refresh_configs
    )


def test():
    pass
