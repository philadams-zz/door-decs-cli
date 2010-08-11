#!/usr/bin/env python

"""
Phil Adams (http://philadams.net)

what this code does
"""

import logging

from PIL import Image, ImageOps, ImageFont, ImageDraw
import aggdraw

def build_door_tags():
    """TODO: something here"""

    size = (600, 400)
    caption_height = 100

    # read in bg image and add transparent strip
    original = Image.open('baker_tower.jpg')
    if original.mode != 'RGBA':
        original = original.convert('RGBA')
    img = original.copy()
    img = ImageOps.fit(img, size)

    canvas = aggdraw.Draw(img)
    brush = aggdraw.Brush('white', opacity=125)
    canvas.rectangle((0, img.size[1]-caption_height, size[0], size[1]), brush)
    canvas.flush()

    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype('/Library/Fonts/HoboStd.otf', 62)
    text = 'alixandria'
    x, y = font.getsize(text)
    canvas.text((size[0]/2 - x/2, size[1] - caption_height/2 - y/2.75),
                text, font=font, fill=0)

    img.show()

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
