Phil Adams (http://philadams.net)

Build pretty looking doortags for dorm residents.
Takes a background image, a csv file of residents, and generates a
PDF file with four tags per page, superimposing the first name and room
number aesthetically on top of the background image.

The csv format is:
<last,first,address,studentID>
where address is understood to be <building roomnumber>
and roomnumber is of the form 0043 or 0102A

An example image and csv file are in /src. The resulting pdf file is in
/gen/the-doortags.pdf

Sample usage:
python doordecs.py src/firefly.jpg src/firefly.csv

Uses standard lib, and PIL, aggdraw, and reportlab packages.
