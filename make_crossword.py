from xml.etree import ElementTree as etree
import argparse

# Cell size
size = 100
# Amount to offset the number by
number_offset = (11, 33)
# Amount to offset the text in the box by
text_offset = (30, 70)

# Giant style string with the CSS for the SVG. problem? no problem.
stylestring = """
    <defs>
    <style type="text/css">
    <![CDATA[
        .stroke {stroke:black;stroke-width:2.22009;stroke-linecap:square}
        .transp {fill:none}
        .black {fill:black}
        .white {fill:white}
        .fnt-times {font-weight:normal;font-size:36;font-family:'Times New Roman'}
        .fnt-museo {font-weight:normal;font-size:64;font-family:'Museo'}
    ]]>
    </style>
    </defs>"""
def translate(coords, offset):
    return map(sum,zip(coords,offset))

def make_cell(col, row, color, text=None, number=None):
    cell = etree.Element("g")
    border = etree.Element("polyline")
    fill = etree.Element("polygon")
    cell.append(border)
    cell.append(fill)
    points = vertices(row, col)
    class_str = "stroke " + color
    border.set("points", points)
    fill.set("points", points)
    border.set("class", class_str)
    fill.set("class", class_str)
    if text is not None:
        textelt = etree.Element("text")
        coords = translate((row * size, col * size), text_offset)
        textelt.set("x", str(coords[0]))
        textelt.set("y", str(coords[1]))
        textelt.set("class", "fnt-museo black")
        textelt.text = str(text)
        cell.append(textelt)
    if number is not None:
        textelt = etree.Element("text")
        coords = translate((row * size, col * size), number_offset)
        textelt.set("x", str(coords[0]))
        textelt.set("y", str(coords[1]))
        textelt.set("class", "fnt-times black")
        textelt.text = str(number)
        cell.append(textelt)
    return cell

def vertices(row, col):
    order = ((0, 0), (0, 1), (1, 1), (1, 0))
    vertices = map (lambda (x,y): ((row + x) * size, (col + y) * size), order)
    return ' '.join(["%s,%s" % vertex for vertex in vertices])

def is_start_of_word(lines, i, j):
    """
    Checks if there is a word starting at (i,j)
    """
    if lines[i][j] == '*':
        return False
    if i == 0 or j == 0:
        return True
    if lines[i-1][j] == '*' and lines[i+1][j] != '*':
        return True
    if lines[i][j-1] == '*' and lines[i][j+1] != '*':
        return True
    return False

def create_svg(lines):
    """Takes a list of lines from a file with newlines stripped and creates a
    SVG
    """
    root = etree.XML('<svg width="100%" height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg"></svg>')
    root.append(etree.XML(stylestring))
    # number is the current word number, for numbering the words in the
    # crossword
    number = 0
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            char = line[j]
            if char == '*':
                # Add a blank black cell
                root.append(make_cell(i, j, 'black'))
            else:
                if is_start_of_word(lines, i, j):
                    number += 1
                    current_number = number
                else:
                    current_number = None
                # Add a white cell, possibly with text
                root.append(make_cell(i, j, 'white', text=char, number=current_number))
    return root


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='make_crossword')
    parser.add_argument('crossword_file', type=str)
    args = parser.parse_args()
    etree.register_namespace("","http://www.w3.org/2000/svg")
    with open(args.crossword_file, 'r') as f:
        lines = [line.strip("\n") for line in f.readlines()]
    svg = create_svg(lines)
    print etree.tostring(svg, encoding='iso-8859-1')

