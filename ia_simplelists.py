#!/usr/bin/env python
"""An 'ia' plugin for simplelists.

Usage: ia simplelists [--help] [--field FIELD] <identifier>

Options:
  -h, --help                Show this help message and exit.
  -f, --field FIELD         Return specific metadata field [default: metadata].

Examples:
    $ ia simplelists --field metadata.title nasa
    NASA Images
"""
from docopt import docopt

# The module name must start with "ia_" in order for it to be recognized as a plugin.
__title__ = __name__
__version__ = '0.0.1'
__url__ = 'https://github.com/jjjake/ia_plugin'
__author__ = 'Jacob M. Johnson'
__email__ = 'jake@archive.org'
__license__ = 'AGPL 3'
__copyright__ = 'Copyright 2015 Internet Archive'
__all__ = [__title__]


# `main()` must include two parameters: `argv` and `session`.
# `argv` is a list of args passed in from `ia`, and `session` is an
# `interenetarchive.ArchiveSession` object. These parameters don't
# necessarily need to be used, necessarily, but must be specified.
def main(argv=None, session=None):
    # Parse the list of args passed in from `ia`.
    args = docopt(__doc__, argv=argv)

    # Write your plugin!
    item = session.get_item(args['<identifier>'])
    fields = args['--field'].split('.')
    md = item.item_metadata
    for f in fields:
        md = md.get(f)
    print(md)

if __name__ == '__main__':
    main()
