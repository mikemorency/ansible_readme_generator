import ansidocs.src.main as ansidocs
import argparse
from os import path
import logging


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel", dest="loglevel", default='WARNING',
                        help="Log level for python logging, defaults " +
                        "to WARNING. Set to WARNING, INFO, DEBUG, ERROR")
    parser.add_argument("-c", "--config-dir", dest="config_dir",
                        help="Path to the config dir",
                        default=path.join(path.expanduser('~'), '.ansidocs'))


    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    gen_parser  = subparsers.add_parser("generate", aliases=["gen"], help="Generate or update an existing readme")
    gen_parser.add_argument("-d", "--directory", dest="directory", default=".",
                        help="Directory where readme should be generated")
    test_parser = subparsers.add_parser("test", help="Test if the existing readme matches the expected readme")

    conf_parser = subparsers.add_parser("config", help="Create or refresh your config directory")
    conf_parser.add_argument("-r", "--refresh-configs", dest="refresh_configs",
                        help="If flag is set, config dir will be removed and recreated with defaults",
                        action='store_true')

    gen_parser.set_defaults(func=gen)
    conf_parser.set_defaults(func=conf)
    test_parser.set_defaults(func=test)

    return parser.parse_args()


def main():
    args = parseArgs()
    logging.basicConfig(level=args.loglevel)
    args.func(args)


def gen(args):
    ansidocs.generate(
        directory=args.directory,
        config_dir=args.config_dir)


def conf(args):
    ansidocs.init_config_dir(
        config_dir=args.config_dir,
        refresh_configs=args.refresh_configs)


def test():
    pass
