# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 22:15:57 2018

@author: irffy
"""

import csv
import matplotlib.pyplot as pltnn
from tkinter import*
with open('london.connections.csv') as v1, open('updated_london.connections.csv', 'w') as v2: #we saved each file speretaely
    next(v1)
    for line in v1:
        v2.write(line) # remove headers
with open('updated_london.connections.csv') as v2:
     network_dict={}
     network_dict2={}
     y = csv.reader(v2)
     u = [] 
     for row in y:
        u.append(row[2])
        if row[2] in network_dict:
            # append the new number to the existing array at this slot
            network_dict[row[2]].append(row[0])
        else:
            network_dict[row[2]] = [row[0]]
        if row[2] in network_dict:
            network_dict[row[2]].append(row[1])
        else:
            network_dict[row[2]] = [row[1]]
        network_values = list(network_dict.values())
with open('updated_london.connections.csv') as v2:
    line_dict ={}
    line_dict2 ={} #create a dictionary of connections for each line from column 0 -1 and from 1-0
    openfile = csv.reader(v2)
    for i in openfile:
        if i[0] in line_dict:
            # append the new number to the existing array at this slot
            line_dict[i[0]].append(i[1])
        else:
            # create a new array in this slot
            line_dict[i[0]] = [i[1]] 
        if i[1] in line_dict2:
            line_dict2[i[1]].append(i[0])
        else:
            line_dict2[i[1]] = [i[0]] 
with open('updated_london.connections.csv') as v2:
    lines ={}
    lines2 ={} #create a dictionary of connections for each line from column 0 -1 and from 1-0
    openfile = csv.reader(v2)
    for i in openfile:
        if i[2] in lines:
            # append the new number to the existing array at this slot
            lines[i[2]].append(i[0])
        else:
            # create a new array in this slot
            lines[i[2]] = [i[0]] 
        if i[2] in lines2:
            lines2[i[2]].append(i[1])
        else:
            lines2[i[2]] = [i[1]] 

    
def merge(*dicts): #function merges dictionaries apending lists of values 
        output_dict = {}
        for dict in dicts:
            for i in dict:
                try:
                    output_dict[i].append(dict[i])
                except KeyError:
                    output_dict[i] = [dict[i]]
        return output_dict


total_lines = merge(lines, lines2)
bakerloo = network_dict.get('1')
circle = network_dict.get('3')
hammersmith_city = network_dict.get('6')
jubilee = network_dict.get('7')
victoria = network_dict.get('11')
central = network_dict.get('2')
district = network_dict.get('4')
east_london = network_dict.get('5')
metropoliton = network_dict.get('8')
northern = network_dict.get('9')
picadilly = network_dict.get('10')
waterloo = network_dict.get('12')
docklands = network_dict.get('13') #run out of time, used brute force to generate lines

def remove_repeat(lists): #removes repeated values in our lists of stations per line
    remove_repeat = []
    for i in lists:
        if i not in remove_repeat:
            remove_repeat.append(i)
    return remove_repeat



    
stations = []   


for i in range(13):
    network_set = list(set(network_values[i]))
    stations.append(network_set)


with open('london.stations.csv') as csv1, open('updated_london.stations.csv', 'w') as csv2:
    next(csv1)
    for line in csv1:
        csv2.write(line)
with open('updated_london.stations.csv') as csv2: # 
    read = csv.reader(csv2)
    latitude = []
    longitude = []
    station_id = []

    for row in read:
        latitude.append(float(row[1]))
        longitude.append((float(row[2]))) #extract list of latitudes and longtitudes to plot
        station_id.append((row[0]))
   
    max_lotd = max(longitude)
    max_latd = max(latitude) #extrtact these values for our normalisation cuntion
    min_lotd = min(longitude)
    min_latd = min(latitude)
    norm_longitude =[]
    norm_latitude = []
    for i in latitude:
        norm = (i - min_latd)*800/(max_latd - min_latd)
        norm_longitude.append(norm)
    for i in longitude:
        norm = (i - min_lotd)*1200/(max_lotd - min_lotd)# normalise our cordinates for size of canvas
        norm_latitude.append(norm)       
    station_loc = list(zip(norm_latitude, norm_longitude))
    station_dict = dict(zip(station_id, station_loc)) #create a dictionary key is each station id and value is its cordinates
    
line_total = merge(line_dict, line_dict2) #total network

def plot_dict(lisst):
    line_list = []
    for i in lisst:
        tempval = list(line_total.get(i))
        line_list.append(tempval)
    dict_output = dict(zip(lisst, line_list))
    return dict_output

def network_graph(dictionary): # funtion will make a dictionary of coordinates in tuples from input 
    dict_keys = list(dictionary.keys())
    dict_values = list(dictionary.values())
    dict_values_flat = []
    dict_value_coords = []
    dict_key_coords = []
    for i in dict_values:
        temp = [item for sublist in i for item in sublist] 
        dict_values_flat.append(temp)
    for i in dict_values_flat:
        value = list(tuple(station_dict[d] for d in i))
        dict_value_coords.append(value)
    for i in dict_keys:
        val = tuple(station_dict[i])
        dict_key_coords.append(val)
    final_dict = dict(zip(dict_keys, dict_values_flat))  
    final_final_dict = dict(zip(dict_key_coords, dict_value_coords))
    return final_final_dict #value returns a complete network graph
network_graph = network_graph(line_total) 
def generate_graph(graph): #funtion to create each distinct connection i.e. every station and its connections are plotted speretaly and in an order such that each stations and its cinnections are plotted
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    net_graph = []
    for i in edges:
        net_graph.append(list(i))
    return net_graph #creates a graph network we can plot onto our gui

net_graph = generate_graph(network_graph)





with open('london.connections.csv') as v1, open('updated_london.connections.csv', 'w') as v2:
    next(v1)
    for line in v1:
        v2.write(line)
with open('updated_london.connections.csv') as v2:
    y = csv.reader(v2) #read csv file in as csv object
    mydict = {} # create dictionary of connections from column 1 - 2
    mydict2 = {} #create dictionary of connections from column 2 - 1
    u = []
    z =[]
    for i in y:
        u.append(i[0]) 
        z.append(i[1])
        if i[0] in mydict:
            # append the new number to the existing array at this slot
            mydict[i[0]].append({i[1]:int(i[3])})
        else:
            # create a new array in this slot
            mydict[i[0]] = [{i[1]:int(i[3])}] # fucntions creates a dictionary of all the connections with associated key i[0]
             # store all these values in a list
        if i[1] in mydict2:
            mydict2[i[1]].append({i[0]:int(i[3])}) #generate all connections from i[1]  t
        else:
            mydict2[i[1]] = [{i[0]:int(i[3])}] 
            connections2 = list(mydict2.values()) #
            listx = []
    
    
    c = merge(mydict, mydict2)
    c_values = list(c.values())
    connecttotal = []
    for i in c_values:
        tempc = [item for sublist in i for item in sublist]
        connecttotal.append(tempc) #flatten list for each value
        
    values = []
    for i in connecttotal:
        values.append({k: v for d in i for k, v in d.items()})
            
    u = list(dict.fromkeys(u)) 
    z = list(dict.fromkeys(z))
    p = u + z
    keys = []
    for i in p:
        if i not in keys:
            keys.append(i)
   # generate total list of stations in apporpriate order to apply trough our dijstras function, removing duplicate values
    global graph
    graph = dict(zip(keys,values))



list1 = []
with open('london.stations.csv') as csv1, open('updated_london.stations.csv', 'w') as csv2:
    next(csv1)
    for line in csv1:
        csv2.write(line)
    with open('updated_london.stations.csv') as csv2:
        reader = csv.reader(csv2)
        all_stations = {i[0]:i[3] for i in reader}
    with open('updated_london.stations.csv') as csv2:
        reader = csv.reader(csv2)
        all_stations2 = {i[3]:i[0] for i in reader}

def dijkstra(graph,start,goal):
    min_weight = {} #shortest pat of possible paths is stroed in a dictionary 
    prev_node = {} 
    nodes = graph
    infinity = 9999999 #set all distances to infinity
    path = [] #output path to list
    for node in nodes:
        min_weight[node] = infinity
    min_weight[start] = 0
 
    while nodes:
        minNode = None
        for node in nodes:
            if minNode is None:
                minNode = node
            elif min_weight[node] < min_weight[minNode]:
                minNode = node
 
        for childNode, weight in graph[minNode].items():
            if weight + min_weight[minNode] < min_weight[childNode]:
                min_weight[childNode] = weight + min_weight[minNode]
                prev_node[childNode] = minNode
        nodes.pop(minNode)
 
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = prev_node[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start) #insert each shortest path into list
    stat_path = []
    for i in path:
        x = all_stations[i]
        stat_path.append(x) #find the station names for each numeric value
        
    if min_weight[goal] != infinity:
        
        print('fastest route is' + str(stat_path)) #if final node is no longeer infnitely far away choose this as the final node and print the path
    

         
root = Tk()

root.title("network interface")
leftframe = Frame(root)
leftframe.pack(side = "left")
right_frame = Frame(root)
right_frame.pack(side = "right" )
cv = Canvas(leftframe ,height="1200",width="1200",bg="white")    
cv.pack(side ="left")
v = StringVar()#create string variable for entry
z = StringVar()

    
    

start = Text(root, height =1, width = 10)
finish = Text(root, height = 1, width = 10 ) #create text input for gui
start.pack()
finish.pack()
def retrieveo():
    global o
    o = start.get("1.0","end-1c")
def retrievep():
    global p
    p = finish.get("1.0", "end-1c")
start_button = Button(root, text = 'start',command =  lambda: retrieveo()).pack()
finish_button = Button(root, text = 'finsih',command = lambda: retrievep() ).pack() #user will see output path in command line, ran out of time to put it on the gui






def station_points(screen_points): 
    """ Function to take list of points and make them into lines
    """
    is_first = True
    # Set up some variables to hold x,y coods
    x0 = y0 = 0
    # Grab each pair of points from the input list
    for (x,y) in screen_points:
        # If its the first point in a set, set x0,y0 to the values
        if is_first:
            x0 = x
            y0 = y
            is_first = False
        else:
            # If its not the fist point yeild previous pair and current pair
            yield x0,y0,x,y
            # Set current x,y to start coords of next line
            x0,y0 = x,y



for i in net_graph:
    
    for (x0,y0, y1,x1) in station_points(i):
        cv.create_line(x0,y0,y1,x1, width=5,fill="red")
    for (x0,y0, y1,x1) in station_points(i):
        cv.create_oval(x0,y0,x0+5,y0+5, width=1,fill="blue")
root.mainloop()

dijkstart = all_stations2[o]
dijkend = all_stations2[p]

dijkstra(graph, dijkstart, dijkend)