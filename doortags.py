#!/usr/bin/env python

"""
Phil Adams (http://philadams.net)

what this code does
"""

import logging
import os

import aggdraw
from PIL import Image, ImageOps, ImageFont, ImageDraw
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus import Image as RLImage

def build_door_tags():
    """TODO: something here"""

    size = (500, 340) # TODO: set good size for doortag
    fontsize = 68
    caption_height = 100
    caption_opacity = 120
    tmp_dir = './gen'
    DPI, PPI = 72, 113 # 113 on the macbook pro...

    # read in bg image and resize
    original = Image.open('baker_tower.jpg')
    img = original.copy()
    img = ImageOps.fit(img, size)

    # draw opaque caption region
    canvas = aggdraw.Draw(img)
    brush = aggdraw.Brush('white', opacity=caption_opacity)
    canvas.rectangle((0, size[1]-caption_height, size[0], size[1]), brush)
    canvas.flush()

    # for each name, grab the first name and add it to a cp of the img
    # save each image to a gen folder

    # add caption
    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype('/Library/Fonts/HoboStd.otf', fontsize)
    text = 'alixandria'
    x, y = font.getsize(text)
    canvas.text((size[0]/2 - x/2, size[1] - caption_height/2 - y/2.75),
                text, font=font, fill=0)

    img.save(os.path.join(tmp_dir, 'abc28_alix-morris.jpg'))

    # arrange the images on a pdf document using tables

    doc = SimpleDocTemplate('doortags.pdf', pagesize=landscape(LETTER))
    elements = []
    table_data = []
    images = os.listdir(tmp_dir)

    # load images as reportlab images
    for image in images:
        table_data.append(RLImage(os.path.join(tmp_dir, image),
        width=size[0]*DPI/PPI, height=size[1]*DPI/PPI))

    # cluster table data into groups of 2 for table cols
    if len(table_data) % 2 != 0:
        table_data.append(table_data[-1])
    table_data = zip(*[iter(table_data)]*2)

    table_styles = [('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6)]
    table = Table(table_data, style=table_styles)
    elements.append(table)

    # build and save the pdf doc
    doc.build(elements)

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
