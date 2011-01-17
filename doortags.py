#!/usr/bin/env python

"""
Phil Adams (http://philadams.net)

Build pretty looking doortags for dorm residents.
Takes a background image, a csv file of residents, and generates a
PDF file with four tags per page, superimposing the first name and room
number aesthetically on top of the background image.

The csv format is:
<last,first,studentID,address>
where address is understood to be <building roomnumber>
and roomnumber is of the form 0043 or 0102A
"""

import logging
import os
import shutil
from csv import reader
from operator import attrgetter

import aggdraw
from PIL import Image, ImageOps, ImageFont, ImageDraw
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus import Image as RLImage

SIZE = (500, 340)
FONTSIZE = 68
SMALLFONTSIZE = 36
CAPTION_HEIGHT = 100
CAPTION_OPACITY = 120
TMP_DIR = './gen'  # should be a child dir of this folder - will get wiped!
DPI, PPI = 72, 113  # 113 on the macbook pro - may need adjusting for you!
PDF_FNAME = 'the-doortags.pdf'


class Student(object):
    """a cornell student"""

    def __init__(self, last, first, address, netid):
        self.last = last
        self.first = first
        self.netid = netid
        self.building, self.roomnumber = address.split()
        self.roomnumber = self.roomnumber[1:]

    def __repr__(self):
        return 'Student<%s, %s (%s)>' % (self.last, self.first, self.netid)


def build_door_tags(bg_fname, student_list):
    """
    build door tags using bg image and list of residents
      - bg_fname: path to background image file
      - students: path to .csv file of residents to build tags for
    """

    # confirm TMP_DIR exists and is empty
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)

    # prepare base image, adding the opaque caption region at bottom
    original = Image.open(bg_fname)
    base_img = original.copy()
    base_img = ImageOps.fit(base_img, SIZE)
    canvas = aggdraw.Draw(base_img)
    brush = aggdraw.Brush('white', opacity=CAPTION_OPACITY)
    canvas.rectangle((0, SIZE[1] - CAPTION_HEIGHT, SIZE[0], SIZE[1]), brush)
    canvas.flush()

    # read in student list
    residents = [Student(*line) for line in reader(open(student_list))]
    residents.sort(key=attrgetter('roomnumber'))

    # set fonts for drawing on base image
    font = ImageFont.truetype('/Library/Fonts/HoboStd.otf', FONTSIZE)
    smallfont = ImageFont.truetype('/Library/Fonts/HoboStd.otf',
                                   SMALLFONTSIZE)

    # for each resident, draw name and room no, and save in TMP_DIR
    for resident in residents:
        tag = base_img.copy()
        canvas = ImageDraw.Draw(tag)
        x, y = font.getsize(resident.first)
        canvas.text((SIZE[0]/2 - x/2, SIZE[1] - CAPTION_HEIGHT/2 - y/2.75),
                    resident.first, font=font, fill=0)
        canvas.text((12, 12), resident.roomnumber, font=smallfont, fill=0)
        fname = '-'.join([resident.roomnumber, resident.netid])
        fname += '.jpg'
        tag.save(os.path.join(TMP_DIR, fname))

    # arrange the images on a pdf document using tables
    doc = SimpleDocTemplate(PDF_FNAME, pagesize=landscape(LETTER))
    table_styles = [('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6)]
    elements = []
    table_data = []
    images = os.listdir(TMP_DIR)
    for image in images:
        table_data.append(RLImage(os.path.join(TMP_DIR, image),
        width=SIZE[0]*DPI/PPI, height=SIZE[1]*DPI/PPI))

    # cluster table data into groups of 2 for table cols
    if len(table_data) % 2 != 0:
        table_data.append(table_data[-1])
    table_data = zip(*[iter(table_data)]*2)

    # build and save the pdf doc
    table = Table(table_data, style=table_styles)
    elements.append(table)
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

    try:
        image, names = args
    except ValueError:
        print('usage: %s path/to/image path/to/residents.csv' % __file__)
        exit()

    build_door_tags(image, names)

if '__main__' == __name__:
    main()
