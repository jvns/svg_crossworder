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


This will generate a filled-in crossword. Originally tt did *not*
generate crossword layouts, it now has a contributed random generator
that takes a long time to run and might give you an output. There is a
sample input file included. The output opens and looks okay to me in
Inkscape. No more promises.

If you want to change the fonts for the numbers or the letters, there
is a stylesheet inside the .py file. You can edit it.

The output looks like this:

![Sample output](http://i.imgur.com/NaAoY1R.png)

To run the generator feed it the words to include it into the
crossword (see sample_generate.txt) and use the command line argument
--generate WxH where W is the number of columns and H is the number of
rows. If there are words that couldn't fit, they are printed to
standard error. You can save the board to a file to finish it by hand
with the command line argument --save_generate <file name>.

![Sample generated output](http://i.imgur.com/cMR0X2R)
