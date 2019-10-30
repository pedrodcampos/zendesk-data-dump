import sys
import argparse

from config import build_zendesk_config
from zendesk import Zendesk
from urllib.parse import quote
from utilities import dump_articles, dump_search


# create the top-level parser
parser = argparse.ArgumentParser(prog='python export.py')
parser.add_argument('--instance', help="Zendesk instance url")
parser.add_argument('--helpcenter', help="Zendesk helpcenter url")
parser.add_argument('--username', help="Admin account user email")
parser.add_argument('--password', help="Admin account password")


subparsers = parser.add_subparsers(
    title='endpoint', required=True, dest='endpoint')
# create the parser for the "a" command
parser_a = subparsers.add_parser(
    'search', help="Download response of a search endpoint request")
parser_a.add_argument('query')
parser_a.add_argument('--filename', help="Change default export filename")

# create the parser for the "b" command
parser_b = subparsers.add_parser(
    'articles', help="Download all articles and related information from a helpcenter")
parser_b.add_argument('--filename', help="Change default export filename")
args = parser.parse_args()

zendesk_config = build_zendesk_config(args.instance, args.helpcenter,
                                      args.username, args.password)
if not all(zendesk_config.values()):
    missing_keys = [key for key, value in zendesk_config.items() if not value]
    sys.exit(f'\nError: missing values for {", ".join(missing_keys)}\n')


zendesk = Zendesk(**zendesk_config)
if args.endpoint == 'articles':
    dump_articles(zendesk, args.filename)
elif args.endpoint == 'search':
    dump_search(zendesk, args.query, include_custom_fields=True,
                filename=args.filename or 'output')
