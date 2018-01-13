#!/usr/bin/env python
"""An 'ia' plugin for simplelists.

Usage:
    ia simplelists <identifier> [options]...
    ia simplelists --help

Options:
  -h, --help            Show this help message and exit.
  -l, --list LIST       The list. [default: disability_access_eligible]
  -p, --parent PARENT   The parent. [default: internet_archive_pd_access]


Examples:

"""
import sys
import json

from docopt import docopt, printable_usage
from schema import Schema, Use, SchemaError
from requests import Request
from internetarchive.auth import S3PostAuth

__title__ = __name__
__version__ = '0.0.1.dev1'
__url__ = 'https://github.com/jjjake/ia_simplelists'
__author__ = 'Jacob M. Johnson'
__email__ = 'jake@archive.org'
__license__ = 'AGPL 3'
__copyright__ = 'Copyright 2015 Internet Archive'
__all__ = [__title__]


def main(argv=None, session=None):
    # Parse the list of args passed in from `ia`.
    args = docopt(__doc__, argv=argv)
    del args['simplelists']

    # Validate and prepare args.
    s = Schema({
        str: Use(bool),
        '<identifier>': str,
        '--parent': Use(lambda p: p[0]),
        '--list': Use(lambda l: l[0]),
    })
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print('{0}\n{1}'.format(str(exc), printable_usage(__doc__)), file=sys.stderr)
        sys.exit(1)

    item = session.get_item(args['<identifier>'])

    # Prepare patch and POST data.
    patch = json.dumps({
        'op': 'set',
        'list': args['--list'],
        'parent': args['--parent'],
    })
    data = {
        '-patch': patch,
        '-target': 'simplelists',
        'priority': '-5',
    }

    # Build request.
    request = Request(
        method='POST',
        url=item.urls.metadata,
        data=data,
        auth=S3PostAuth(session.access_key, session.secret_key),
    )
    prepared_request = request.prepare()

    # TODO: probably ready to uncomment this, and give it a try?
    #r = session.send(prepared_request)
    #if r.status_code == 200 or 'no changes' in r.text:
    #    print('success: {}'.format(item.urls.history))
    #    sys.exit(0)
    #else:
    #    print('error: {} - {} - {}'.format(item.identifier, r.status_code, r.content))
    #    sys.exit(1)

    # TODO: delete
    print('args:\n\n{}\n'.format(args))
    print('item:\n\n{}\n'.format(item))
    print('POST data:\n\n{}'.format(request.data))

if __name__ == '__main__':
    main()
