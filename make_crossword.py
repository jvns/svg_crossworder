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
        .fnt-numbers {font-weight:normal;font-size:36;font-family:'Times New Roman'}
        .fnt-letters {font-weight:normal;font-size:64;font-family:'Courier New'}
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
        textelt.set("class", "fnt-letters black")
        textelt.text = str(text)
        cell.append(textelt)
    if number is not None:
        textelt = etree.Element("text")
        coords = translate((row * size, col * size), number_offset)
        textelt.set("x", str(coords[0]))
        textelt.set("y", str(coords[1]))
        textelt.set("class", "fnt-numbers black")
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
    left = '*' if i == 0  else lines[i-1][j]
    right = '*' if (i == len(lines) - 1) else lines[i+1][j]
    above = '*' if j == 0  else lines[i][j - 1]
    below = '*' if j == len(lines[i]) - 1  else lines[i][j+1]
    if left == '*' and right != '*':
        return True
    if above == '*' and below != '*':
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

def generate(words, geometry, save_to):
    import sys
    import random
    
    (w,h) = map(int,geometry.split("x"))
    board = []
    for i in xrange(0,h):
        board.append("*" * w)

    # random!
    iterations = 1000
    first = True
    while iterations and words:
        iterations -= 1
        random.shuffle(words)
        word = words[-1]

        #print >>sys.stderr, word

        # potential places with contact
        places = []
        for i in xrange(0,h):
            for j in xrange(0,w):
                if first:
                    places.append( (i,j) )
                elif board[i][j] in word:
                    for p in xrange(0, len(word)):
                        if word[p] == board[i][j]:
                            #print >>sys.stderr, i, j, p, word[p]
                            if i-p >=0:
                                places.append( (i-p,j) )
                            if j-p >=0:
                                places.append( (i,j-p) )

        if not places:
            continue
        
        pos = random.choice(places)
        #print >>sys.stderr, pos
        dirs = []
        if pos[0] + len(word) < h:
            dirs.append("V")
        if pos[1] + len(word) < w:
            dirs.append("H")
        random.shuffle(dirs)

        #print >>sys.stderr, dirs

        good = False
        for dir in dirs:
            
            board_copy = []
            for line in board:
                board_copy.append(list(line))
                
            (x,y) = pos
            found_error = False
            has_contact = False

            if dir == "V":
                for p in xrange(0, len(word)):
                    if p == 0 and x > 0 and board_copy[x-1][y] != '*':
                        found_error = True
                        break
                    if p == len(word) -1 and x < h-1 and board_copy[x+1][y] != '*':
                        found_error = True
                        break
                    
                    if not(board_copy[x][y] == '*' or board_copy[x][y] == word[p]):
                        found_error = True
                        break

                    contact_here = False
                    if board_copy[x][y] == word[p]:
                        has_contact = True
                        contact_here = True
                        
                    if y < w-1 and board_copy[x][y+1] != '*' and not contact_here:
                        found_error = True
                        break
                    if y > 0 and board_copy[x][y-1] != '*' and not contact_here:
                        found_error = True
                        break
                        
                    board_copy[x][y] = word[p]
                    x += 1

            if dir == "H":
                for p in xrange(0, len(word)):
                    if p == 0 and y > 0 and board_copy[x][y-1] != '*':
                        found_error = True
                        break
                    if p == len(word) -1 and y < w-1 and board_copy[x][y+1] != '*':
                        found_error = True
                        break
                    
                    if not(board_copy[x][y] == '*' or board_copy[x][y] == word[p]):
                        found_error = True
                        break
                    
                    contact_here = False
                    if board_copy[x][y] == word[p]:
                        has_contact = True
                        contact_here = True
                        
                    if x < h-1 and board_copy[x+1][y] != '*' and not contact_here:
                        found_error = True
                        break
                    if x > 0 and board_copy[x-1][y] != '*' and not contact_here:
                        found_error = True
                        break
                        
                    board_copy[x][y] = word[p]
                    y += 1

            #print >>sys.stderr, "\n".join(map(lambda x:"".join(x),board_copy))+"\n"

            if not found_error and (first or has_contact):
                #print >>sys.stderr, "success!"
                good = True
                board = board_copy
                break
            
        if good:
            del words[-1]
            first = False

    if words:
        print >>sys.stderr, "words remaining: ", words
    
    if save_to:
        with open(save_to,"w") as f:
            f.write("\n".join(map(lambda x:"".join(x),board))+"\n")
            
    return board
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='make_crossword')
    parser.add_argument('crossword_file', type=str)
    parser.add_argument('--generate', type=str, default=None)
    parser.add_argument('--save_generated', type=str, default=None)
    args = parser.parse_args()
    etree.register_namespace("","http://www.w3.org/2000/svg")
    with open(args.crossword_file, 'r') as f:
        lines = [line.strip("\n") for line in f.readlines()]
    if args.generate:
        lines = generate(lines, args.generate, args.save_generated)
    svg = create_svg(lines)
    print etree.tostring(svg, encoding='iso-8859-1')

