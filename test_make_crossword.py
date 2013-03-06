from xml.etree import ElementTree as etree
from make_crossword import vertices, make_cell

def test_vertices():
    assert vertices(2,6) == "200,600 200,700 300,700 300,600"
