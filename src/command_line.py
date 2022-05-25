import src.update_readme
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel", dest="loglevel", default='WARNING',
                        help="Log level for python logging, defaults " +
                        "to WARNING. Set to WARNING, INFO, DEBUG, ERROR")
    parser.add_argument("-d", "--directory", dest="directory", default=".",
                        help="Directory where readme should be generated")
    parser.add_argument("-f", "--readmefile", dest="readme_file",
                        help="Readme file name", default='README.md')

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    gen_parser  = subparsers.add_parser("generate", aliases=["gen"], help="Generate or update an existing readme")
    test_parser = subparsers.add_parser("test", help="Test if the existing readme matches the expected readme")

    gen_parser.set_defaults(func=main)

    test_parser.set_defaults(func=test)

    return parser.parse_args()

def main():
    args = parseArgs()
    src.update_readme.main(directory=args.directory, loglevel=args.loglevel)

def test():
    pass
