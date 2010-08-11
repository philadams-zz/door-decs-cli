#!/usr/bin/env python

"""
Phil Adams (http://philadams.net)

what this code does
"""

import logging

from PIL import Image, PSDraw

def build_door_tags():
    """TODO: something here"""

    # read in bg image and add transparent strip
    # for each name, grab the first name and add it to a cp of the img
    # arrange the images on a pdf document

def main():
    """called with __name__ run as __main__"""
    import optparse

    # populate options
    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help='increase verbosity (specify multiple times for more)')
    # parse the arguments (defaults to parsing sys.argv)
    opts, args = optp.parse_args()

    # check incoming opts and call optp.error('msg') to exit if all not well

    # logging config
    log_level = logging.WARNING  # default
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose >= 2:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    build_door_tags()

if '__main__' == __name__:
    main()
