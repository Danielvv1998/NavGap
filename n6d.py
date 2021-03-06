import csv
import os
import time
import tkinter
import subprocess
#import commands

#graph = {'RPI_AP1':{'RPI_AP2':1, 'RPI_AP3':3, 'RPI_DB': 1},'RPI_AP2':{'RPI_AP1':1, 'RPI_AP4':2, 'RPI_DB':1}, 'RPI_AP3':{'RPI_AP1':3, 'RPI_AP4':10}, 'RPI_AP4': {'RPI_AP3':10, 'RPI_AP2':2}, 'RPI_DB': {'RPI_AP1':1, 'RPI_AP2':1}}   #imported from db
#start = input('Enter start location: ')
routeList = []

End = ''

#spotdict name : [connection, strength, loc X, loc Y], node gets appended behind it once the script starts
spotDict = {
    #primary pi's
    'RPI_AP1' : [False, 0, 95, 80],
    'RPI_AP2' : [False, 0, 170, 80],
    'RPI_AP3' : [False, 0, 170, 160],
    'RPI_AP4' : [False, 0, 95, 160],
    'RPI_DB' : [False, 0, 130, 120],

    #extention pi's
    'RPI_AP5' : [False, 0, 130, 190],
    'RPI_AP6' : [False, 0, 95, 225],
    'RPI_AP7' : [False, 0, 170, 225],
    'RPI_AP8' : [False, 0, 240 , 160],
    'RPI_AP9' : [False, 0, 200, 120],
    'RPI_AP10' : [False, 0, 240, 80],
    'RPI_AP11' : [False, 0, 265, 120],
    'RPI_AP12' : [False, 0, 295 , 160],
    'RPI_AP13' : [False, 0, 295, 80],
    'RPI_AP14' : [False, 0, 200, 60],
    'RPI_AP15' : [False, 0, 225, 40],
    'RPI_AP16' : [False, 0, 170 , 40],
    'RPI_AP17' : [False, 0, 130, 60],
    'RPI_AP18' : [False, 0, 95, 40]
}

e = 'RPI_AP'
connectDict = {
    #primary pi's
    'RPI_AP1' : ['RPI_AP2', 'RPI_AP4', 'RPI_AP18', 'RPI_AP17'],
    'RPI_AP2' : ['RPI_AP1', 'RPI_AP17', 'RPI_AP16', e+'14', e+'10', e+'9', e+'3', 'RPI_DB'],
    'RPI_AP3' : [e+'7', e+'5', e+'4', 'RPI_DB', e+'2', e+'9', e+'8'],
    'RPI_AP4' : [e+'3', e+'5', e+'6', e+'1'],
    'RPI_DB' :  [e+'2', e+'17', e+'9', e+'3', e+'5'],

    #extention pi's
    'RPI_AP5' : [e+'6', e+'4', 'RPI_DB', e+'3', e+'7'],
    'RPI_AP6' : [e+'4', e+'5', e+'7'],
    'RPI_AP7' : [e+'6', e+'5', e+'3'],
    'RPI_AP8' : [e+'3', e+'9', e+'10', e+'11', e+'12'],
    'RPI_AP9' : ['RPI_DB', e+'2', e+'14', e+'10', e+'11', e+'8', e+'3'],
    'RPI_AP10' : [e+'2', e+'14', e+'10', e+'13', e+'11', e+'9'],
    'RPI_AP11' : [e+'9', e+'10', e+'13', e+'12', e+'8'],
    'RPI_AP12' : [e+'8', e+'11', e+'13'],
    'RPI_AP13' : [e+'10', e+'11', e+'12'],
    'RPI_AP14' : [e+'17', e+'16', e+'15', e+'10', e+'9', e+'2'],
    'RPI_AP15' : [e+'16', e+'10', e+'14'],
    'RPI_AP16' : [e+'18', e+'15', e+'14', e+'2', e+'17'],
    'RPI_AP17' : [e+'18', e+'16', e+'14', e+'2', 'RPI_DB', e+'1'],
    'RPI_AP18' : [e+'1', e+'17', e+'16']
}

#graph = {'RPI_AP1':{'RPI_AP2':1, 'RPI_AP3':3, 'RPI_DB': 1}}
graph = {
    #primary pi's
    'RPI_AP1' : {'RPI_AP2':1, 'RPI_AP4':1, 'RPI_AP18':1, 'RPI_AP17':1},
    'RPI_AP2' : {'RPI_AP1':1, 'RPI_AP17':1, 'RPI_AP16':1, e+'14':1, e+'10':1, e+'9':1, e+'3':1, 'RPI_DB':1},
    'RPI_AP3' : {e+'7':1, e+'5':1, e+'4':1, 'RPI_DB':1, e+'2':1, e+'9':1, e+'8':1},
    'RPI_AP4' : {e+'3':1, e+'5':1, e+'6':1, e+'1':1},
    'RPI_DB' :  {e+'2':1, e+'17':1, e+'9':1, e+'3':1, e+'5':1},

    #extention pi's
    'RPI_AP5' : {e+'6':1, e+'4':1, 'RPI_DB':1, e+'3':1, e+'7':1},
    'RPI_AP6' : {e+'4':1, e+'5':1, e+'7':1},
    'RPI_AP7' : {e+'6':1, e+'5':1, e+'3':1},
    'RPI_AP8' : {e+'3':1, e+'9':1, e+'10':1, e+'11':1, e+'12':1},
    'RPI_AP9' : {'RPI_DB':1, e+'2':1, e+'14':1, e+'10':1, e+'11':1, e+'8':1, e+'3':1},
    'RPI_AP10' : {e+'2':1, e+'14':1, e+'10':1, e+'13':1, e+'11':1, e+'9':1},
    'RPI_AP11' : {e+'9':1, e+'10':1, e+'13':1, e+'12':1, e+'8':1},
    'RPI_AP12' : {e+'8':1, e+'11':1, e+'13':1},
    'RPI_AP13' : {e+'10':1, e+'11':1, e+'12':1},
    'RPI_AP14' : {e+'17':1, e+'16':1, e+'15':1, e+'10':1, e+'9':1, e+'2':1},
    'RPI_AP15' : {e+'16':1, e+'10':1, e+'14':1},
    'RPI_AP16' : {e+'18':1, e+'15':1, e+'14':1, e+'2':1, e+'17':1},
    'RPI_AP17' : {e+'18':1, e+'16':1, e+'14':1, e+'2':1, 'RPI_DB':1, e+'1':1},
    'RPI_AP18' : {e+'1':1, e+'17':1, e+'16':1}
}

userList = []

## updates the list of connections ##
def updateList():
    global spotDict
    global userList
    #appendLog("# updating list", updateList.__name__)
    updateCmd = 'sudo iwlist wlan0 scan |grep -e Signal -e ESSID'

    trueCount = 0
    ## use this when testing on pi
    # result = subprocess.getoutput(updateCmd)
    # if len(result) > 0:
    #     userList = []
    #     for spot in spotDict:
    #         row = 0
    #         for line in result.split('\n'):
    #             row += 1
    #             essid = line[27:-1]
    #             signal = line[49:51]
    #             #print(essid)
    #             #print(signal)
    #             if row % 2 == 1:
    #                 rowdata = signal
    #                 #print(rowdata)
    #             if essid == spot and int(rowdata) <= 70: # -75 = range limiter
    #                 print('{} set to true, breaking for loop, current str: {}'.format(essid, rowdata))
    #                 spotDict[spot][0] = True
    #                 spotDict[spot][1] = rowdata
    #                 userList.append(essid)
    #                 appendLog("setting spot '{}' to True in spotDict".format(spot), updateList.__name__)
    #                 break
    #             else:
    #                 if spotDict[spot][0] == True and essid == spot:
    #                     print('{} set to false, last str: {}'.format(essid, rowdata))
    #                 spotDict[spot][0] = False
    #                 #print('{} set to false'.format(essid))
    #                 appendLog("setting spot '{}' to False in spotDict".format(spot), updateList.__name__)
    # print('user inbetween: {}'.format(userList))

    ## this is for pc testing, rips info from old log
    # if os.name == 'nt':
    userList = []
    for spot in spotDict:
        #print(' | Connection: {:15}: {}, strength: {}'.format(spot, spotDict[spot][0], spotDict[spot][1]))
        with open('log.csv', 'r') as file:
            reader = csv.reader(file)
            row = 0
            for line in reader:
                row += 1
                essid = line[0][27:-1]
                signal = line[0][49:51]
                #print(spot)
                #print(essid)
                if row % 2 == 1:
                    rowdata = signal
                    #print(rowdata)
                if essid == spot and int(rowdata) <= 75: # range limiter
                    if spotDict[spot][0] == False:
                        #print('{} found, set to true'.format(essid))
                        spotDict[spot][0] = True
                        spotDict[spot][1] = rowdata
                        userList.append(essid)
                    break
                else:
                    spotDict[spot][0] = False
                    #print('{} set to false'.format(essid))
    #print('user inbetween: {}'.format(userList))
    appendLog("user location = {}".format(userList), createUI.__name__)

## GUI ##
blue = '#08088A'
yellow = '#FFFF00'
red = '#FF0000'
green = '#3ADF00'
running = False


def createOval(canvas, spotName, x, y):
    ovalSize = 8
    appendLog("creating node @ {}x, {}y".format(x, y), createOval.__name__)
    #print('creating {} (node) on {} at {}, {}'.format(spotName, canvas, x, y))
    nodeLoc = [
        [(x-ovalSize), (y-ovalSize)],
        [(x+ovalSize), (y+ovalSize)]
    ]
    create = canvas.create_oval(nodeLoc[0][0], nodeLoc[0][1], nodeLoc[1][0], nodeLoc[1][1], fill=blue, activefill=red)
    global spotDict
    createLabel = canvas.create_text(x, (y+20), text=spotName)
    #nodeDict[nodeName] = [create, x, y]
    #spotDict[spotName].append([create, x, y])
    spotDict[spotName].append([create, createLabel, x, y])
    canvas.bind('<ButtonPress-1>', onObjectClick)

def createUser(canvas, x, y):
    appendLog("creating user @ {}x, {}y".format(x, y), createUser.__name__)
    ovalSize = 4
    #print('creating (solo node) at {}, {}'.format(x, y))
    nodeLoc = [
        [(x-ovalSize), (y-ovalSize)],
        [(x+ovalSize), (y+ovalSize)]
    ]
    global user
    user = canvas.create_oval(nodeLoc[0][0], nodeLoc[0][1], nodeLoc[1][0], nodeLoc[1][1], fill=green, activefill=red)

def createConnection(canvas, point1, point2):
    # (x1, y1, x2, y2)
    appendLog("creating connection between '{}' {}x, {}y and '{}' {}x, {}y".format(point1,
                                                                               spotDict[point1][2], spotDict[point1][3],
                                                                               point2,
                                                                               spotDict[point2][2], spotDict[point2][3]), createConnection.__name__)
    # print('creating connection between {} at x{},y{} and {} at x{},y{}'.format(point1,
    #                                                                            spotDict[point1][2], spotDict[point1][3],
    #                                                                            point2,
    #                                                                            spotDict[point2][2], spotDict[point2][3]))
    canvas.create_line(spotDict[point1][2], spotDict[point1][3], spotDict[point2][2], spotDict[point2][3])

def createRoute(point1, point2, color):
    global canvas
    # (x1, y1, x2, y2)
    appendLog("creating Dijkstra between '{}' {}x, {}y and '{}' {}x, {}y".format(point1,
                                                                               spotDict[point1][2], spotDict[point1][3],
                                                                               point2,
                                                                               spotDict[point2][2], spotDict[point2][3]), createRoute.__name__)
    line = canvas.create_line(spotDict[point1][2], spotDict[point1][3], spotDict[point2][2], spotDict[point2][3], fill=yellow, arrow=tkinter.LAST, arrowshape=[10,10,5], width=3)
    global routeList
    routeList.append(line)
    print(routeList)

def routeLiner(path):
    global canvas
    #print("Lining Path")
    appendLog("# lining path".format(), routeLiner.__name__)

    print(path)
    counter = 0
    for each in path:
        if counter < len(path)-1:
            #print('create path between {} and {}'.format(path[counter], path[counter+1]))
            createRoute(path[counter], path[counter+1], red)
            routeList = []
        counter += 1


def updateUser(canvas, user, points):
    pointList = []
    for each in points:
        pointList.append([each, int(spotDict[each][1])])

    sortedPointList = sorted(pointList, key=lambda point: point[1])
    appendLog("updating user loc", updateUser.__name__)

    if len(pointList) > 0:
        point1 = spotDict[sortedPointList[0][0]]
        point1x, point1y = spotDict[sortedPointList[0][0]][2], spotDict[sortedPointList[0][0]][3]
        if len(pointList) > 1:
            point2x, point2y = spotDict[sortedPointList[1][0]][2], spotDict[sortedPointList[1][0]][3]
            if len(pointList) > 2:
                point3x, point3y = spotDict[sortedPointList[2][0]][2], spotDict[sortedPointList[2][0]][3]

        newUserX, newUserY = 0, 0

        print(pointList)
        print(sortedPointList[0][0])
        print(spotDict[sortedPointList[0][0]][2])
        print()
        global start
        start = sorted(pointList, key=lambda point: point[1])[0][0]

        # A>B?
        # Bx - Ax = Dif
        # Bx - (dif/2) = newX

        # calculate new x
        if len(pointList) > 2:
            if point2x > point3x:
                dif = point2x - point3x
                newUserX = point2x - (dif/2)
            else:
                dif = point3x - point2x
                newUserX = point3x - (dif/2)
        if len(pointList) > 1:
            if newUserX > 0:
                if newUserX > point1x:
                    dif = newUserX - point1x
                    newUserX = newUserX - (dif/2)
                else:
                    dif = point1x - newUserX
                    newUserX = point1x - (dif/2)
            else:
                if point1x > point2x:
                    dif = point1x - point2x
                    newUserX = point1x - (dif/2)
                else:
                    dif = point2x - point1x
                    newUserX = point2x - (dif/2)
        else:
            if point1x > 0:
                newUserX = point1x
            else:
                newUserX = 50


        # calculate new y
        if len(pointList) > 2:
            if point2y > point3y:
                dif = point2y - point3y
                newUserY = point2y - (dif/2)
            else:
                dif = point3y - point2y
                newUserY = point3y - (dif/2)
        if len(pointList) > 1:
            if newUserY > 0:
                if newUserY > point1y:
                    dif = newUserY - point1y
                    newUserY = newUserY - (dif/2)
                else:
                    dif = point1y - newUserY
                    newUserY = point1y - (dif/2)

            else:
                if point1y > point2y:
                    dif = point1y - point2y
                    newUserY = point1y - (dif/2)
                else:
                    dif = point2y - point1y
                    newUserY = point2y - (dif/2)
        else:
            if point1y > 0:
                newUserY = point1y
            else:
                newUserY = 50

        #print('new user coords: x{}, y{}'.format(newUserX, newUserY))
        if sortedPointList[0][1] < 60:
            newUserX, newUserY = point1x, point1y
            if sortedPointList[0][0] == End:
                resetRoute()

        ovalSize = 4
        nodeLoc = [
            [newUserX-ovalSize, newUserY-ovalSize],
            [newUserX+ovalSize, newUserY+ovalSize]
        ]
        appendLog("placing user @ {}x, {}y".format(newUserX, newUserY), updateUser.__name__)
        canvas.coords(user, nodeLoc[0][0], nodeLoc[0][1], nodeLoc[1][0], nodeLoc[1][1])


    #canvas.coords(user, xCoords[-1], yCoords[-1])

def changeNodeColor(canvas, spotName, color):
    canvas.itemconfig(spotDict[spotName][-1][0], fill=color)

def stopApp(tkroot):
    """
    Summary:
    Sets running on False, which stops the while loop.
    Then it destroys the root and shutsdown the application.
    :param tkroot:
    The Tkinter application
    :return:
    """
    #print('killing root')
    appendLog("ending app", stopApp.__name__)

    running = False
    tkroot.destroy()
    tkroot.quit()

def updateNodes(canvas):
    """
    Summary:
    Checks for each spot in spotDict if it has signal / is in reach / is True.
    If so, the node color changes to yellow.
    Else the node color changes to blue.
    :param canvas:
    The tkinter canvas on which the nodes will be updated
    :return:
    """
    for each in spotDict:
        if spotDict[each][0] == True:
            changeNodeColor(canvas, each, yellow)
        else:
            changeNodeColor(canvas, each, blue)

def resetRoute():
    """
    Summary:
    Removes current routeList and deletes each line on that route.
    :return:
    """
    global routeList, canvas
    for each in routeList:
        canvas.delete(each)
    routeList = []


def onObjectClick(event):
    """
    Summary:
    Resets the current route on screen when a new destination is selected.
    Registers a click on the screen with it's x- an y-coordinates,
    then finds the closest canvas widget. If the closest canvas widget is an oval / node, that oval will be the new end. (=destination)
    :param event:
    The click on the screen
    :return:
    """
    global routeList
    resetRoute()
    #print('Got object click', event.x, event.y)
    appendLog("Got object click {}x, {}y".format(event.x, event.y), onObjectClick.__name__)
    for each in spotDict:
        #print('if {} == {}'.format(event.widget.find_closest(event.x, event.y)[0], spotDict[each][4][0]))
        if int(event.widget.find_closest(event.x, event.y)[0]) == int(spotDict[each][4][0]):
            #print("closest: " + str(each))
            global end
            end = each
    #appendLog("ending app", stopApp.__name__)
    appendLog("start {}, end {}".format(start, end), appendLog.__name__)
    routeLiner(dijkstra(graph, start, end))


def createLog():
    """
    Summary:
    Creates a new empty log with the current date as name.
    """
    logName = 'NGAPP_LOG_' + time.strftime("%d%m%y")+ '.txt'
    with open(logName, 'w') as file:
        file.close()

def appendLog(string, function):
    """
    Summary:
    Appends a row to the log with the current time, the function and the message.
    :param string:
    The message in a string that will be appended to the log
    :param function:
    The function where the message is coming from
    Example:
    03:46:52-[createUI] creating UI with 420x, 300y, fullscreen. Backgroundimage = backgrond.gif
    :return:
    """
    logName = 'NGAPP_LOG_' + time.strftime("%d%m%y") + '.txt'
    with open(logName, 'a') as file:
        file.write(time.strftime('%I:%M:%S')+'-[{}] {}\n'.format(function, string))
        file.close()

##### DIJKSTRA ALGORITHM #####
def dijkstra(graph_dict, start, end):
    """
    Returns the shortest route from the starting node to the ending node according to the information in graph_dict.
    :param graph_dict:
    A dictionary with for each node another dictionary with the nodes connected to that node and the distance between them.
    Example : {A:{B:1, C:2}, B:{A:1, C:1}, C:{B:1, A:2}
    :param start:
    Starting node in spotDict
    :param end:
    Destination node in spotDict
    :return:
    """
    global End
    End = end

    #print("Graph used: ",graph_dict)
    appendLog("Dijkstra graph used: {}".format(graph_dict), stopApp.__name__)
    # create empty dictionary to hold the distance of each node to the start node
    distances = {}

    # create empty dict to hold the predecessor of each node
    predecessors = {}

    # set all initial distances to infinity and all predecessor None
    for node in graph_dict:
        distances[node] = float('inf')
        predecessors[node] = None
    # create empty list for nodes that have been visited with permanent distance
    labelled_nodes = []

    # set the distance from the start node to be 0
    distances[start] = 0

    # as long as there are still nodes to assess:
    while len(labelled_nodes) < len(graph_dict):

        # create empty dict for nodes that are still available
        still_in = {}
        for node in graph_dict:
            if node not in labelled_nodes:
                still_in[node] = distances[node]

        # find the node with the lowest distance to the current node
        lowest = float('inf')
        for each in still_in:
            if still_in.get(each) < lowest:
                lowest = still_in[each]
                closest = each
        # and add it to the permanently labelled nodes
        labelled_nodes.append(closest)

        # if node is a neighbor of closest
        for node in graph_dict[closest]:
            if graph_dict[closest][node] != None:
                # if a shorter path to that node can be found
                if distances[node] > distances[closest] + graph_dict[closest][node]:
                # update the distance with that shorter distance
                    distances[node] = distances[closest] + graph_dict[closest][node]
                # set the predecessor for that node
                    predecessors[node] = closest

    path = [end]
    while start not in path:
        path.append(predecessors[path[-1]]) #find and append the predecessor of the last node in path
    # return the path
    return path[::-1]

##### UI LOOP #####
def createUI():
    running = True
    WIDTH, HEIGHT = 420, 300
    root = tkinter.Tk()
    bgImage = tkinter.PhotoImage(file='background.gif')
    global canvas
    canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    background = canvas.create_image((WIDTH/2),(HEIGHT/2), image=bgImage)
    # root.overrideredirect(True)
    # root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    appendLog("creating UI with {}x, {}y, fullscreen. Backgroundimage = {}".format(WIDTH, HEIGHT, 'backgrond.gif'), createUI.__name__)

    appendLog("# creating grid", createUI.__name__)
    for con in connectDict:
        for link in connectDict[con]:
            #appendLog("# creating grid", createUI.__name__)
            createConnection(canvas, con, link)

    appendLog("# creating nodes", createUI.__name__)
    for each in spotDict:
        createOval(canvas, each, spotDict[each][2], spotDict[each][3])

    appendLog("# creating buttons".format(WIDTH, HEIGHT, 'backgrond.gif'), createUI.__name__)
    exit = tkinter.Button(text='exit', command=lambda :stopApp(root))
    exit_place = canvas.create_window(20, 30, window=exit)

    createUser(canvas, WIDTH/2, HEIGHT/2)
    counter = 0

    while running:
        if counter > 2:
            updateList()
            counter = -1
            time.sleep(0.1)
            updateUser(canvas,user, userList)

        updateNodes(canvas)
        root.update_idletasks()
        root.update()
        counter += 1


## app boot loop ##
while True:
    print('running on {}'.format(os.name)) # windows = nt, rpi = posix
    appendLog('', '')
    appendLog('', '')
    appendLog('## Application Boot', '')
    appendLog("## running on {}".format(os.name), '')
    updateList()
    start = 'RPI_DB'
    print(spotDict)
    # text = input(' | null = update list \n | break = nuke app \n | start = start app \n >')
    # if text == 'break':
    #     break
    # elif text == 'start':
    #     createUI()

    createUI()
