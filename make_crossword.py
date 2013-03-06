from xml.etree import ElementTree as etree

size = 100
number_offset = (11, 33)
text_offset = (30, 70)

def translate(coords, offset):
    return map(sum,zip(coords,offset))

def make_cell(row, col, color, text=None, number=None):
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

def is_number(lines, i, j):
    if lines[i][j] == '*':
        return False
    if i == 0 or j == 0:
        return True
    if lines[i-1][j] == '*' and lines[i+1][j] != '*':
        return True
    if lines[i][j-1] == '*' and lines[i][j+1] != '*':
        return True
    return False
if __name__ == '__main__':
    etree.register_namespace("","http://www.w3.org/2000/svg")
    root = etree.XML('<svg width="100%" height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg"></svg>')
    defs = """
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
    root.append(etree.XML(defs))
    root.append(etree.Element("path"))
    with open('input.txt') as f:
        number = 0
        lines = [line.strip("\n") for line in f.readlines()]
        for i in range(len(lines)):
            line = lines[i]
            for j in range(len(line)):
                char = line[j]
                if char == '*':
                    root.append(make_cell(j, i, 'black'))
                else:
                    if is_number(lines, i, j):
                        number += 1
                        current_number = number
                    else:
                        current_number = None
                    root.append(make_cell(j, i, 'white', text=char, number=current_number))
            i += 1
    print etree.tostring(root, encoding='iso-8859-1')

