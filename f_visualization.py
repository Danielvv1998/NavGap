import time
import tkinter
#coords between (10,10) and (415, 295), otherwise it won't be drawn ON the canvas
coordA = [90, 180]
coordB = [50, 70]
coordC = [120, 200]
ovalSize = 8

path = ['B', 'A', 'C']

def createOval(coord):
    global node
    tempCoord = coord.copy()
    tempCoord1 = coord.copy()
    node = [[], []]
    counter = 0
    for each in coord:
        if counter == 0:
            tempCoord[0] -= ovalSize
            node[0].append(tempCoord[0])
            tempCoord[1] -= ovalSize
            node[0].append(tempCoord[1])
            counter += 1
        else:
            tempCoord1[0] += ovalSize
            node[1].append(tempCoord1[0])
            tempCoord1[1] += ovalSize
            node[1].append(tempCoord1[1])


blue = '#08088A'
yellow = '#FFFF00'
red = '#FF0000'

def createUI():
    base = tkinter.Tk()
    running = True
    WIDTH = 420
    HEIGHT = 300
    canvas = tkinter.Canvas(base, width=WIDTH, height=HEIGHT)
    canvas.grid()

    createOval(coordA)
    o = canvas.create_oval(node[0][0], node[0][1], node[1][0], node[1][1], fill=blue, activefill=red)

    createOval(coordB)
    o1 = canvas.create_oval(node[0][0], node[0][1], node[1][0], node[1][1], fill=blue, activefill=red)
    createOval(coordC)
    o1 = canvas.create_oval(node[0][0], node[0][1], node[1][0], node[1][1], fill=blue, activefill=red)

    lineAB = canvas.create_line(coordB[0], coordB[1], coordA[0], coordA[1])
    lineAC = canvas.create_line(coordC[0], coordC[1], coordA[0], coordA[1])
    LineCB = canvas.create_line(coordC[0], coordC[1], coordB[0], coordB[1])

    canvas.create_text(240, 44)
    textA = canvas.itemconfig(canvas.create_text(coordA[0], coordA[1]), text="A", fill=yellow)
    textB = canvas.itemconfig(canvas.create_text(coordB[0], coordB[1]), text="B", fill=yellow)
    textC = canvas.itemconfig(canvas.create_text(coordC[0], coordC[1]), text="C", fill=yellow)


    while running == True:
        base.update_idletasks()
        base.update()

createUI()
