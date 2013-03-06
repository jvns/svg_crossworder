SVG Crossword maker
===================

This is a short script I wrote this evening to make SVG crosswords.

Run it like this:

    python make\_crossword.py input.txt > my\_crossword.svg

where input.txt looks like this:

    *pa*
    test
    *s*i
    *t*e

This will generate a filled-in crossword. It does *not* generate
crossword layouts. There is a sample input file included.

If you want to change the fonts for the numbers or the letters, there
is a stylesheet inside the .py file. You can edit it.
