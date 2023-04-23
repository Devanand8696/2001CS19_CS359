"""
Author : V.Sai Vardhan
Roll No. : 2001CS58
"""



# Import all necessary libraries
import numpy as np
import queue                               #To use queue data types while using threads
import time                                #Library to make the threads wait
import threading                           #Library for threading
from tabulate import tabulate              #Helps to print tables

"""************************************************************************************************************************************************"""
file = open("topology.txt", "r")           #File descriptor for opening the file
N =0                                       #Varable to take in the no. of routers
Routers =[]                                #Contains list of routers
ind=0                                      #Index of lines in file
Edges = []                                 #Dictionary to hold all the neigbours of a router
RouterId ={}                               #Dictionary to store the position of a router in "Routers" list. E.g if Routers[0] ='A' , then RouterId['A'] = 0
SQueue = {}                                #Dictinary to hold the shared queue of a router, where in all its neghbours will push their vector table
Neighbors = {}                             #Temporrary list to take in line of edges from files
lock = threading.Lock()                    #Initiating lock variables

"""************************************************************************************************************************************************"""
#Take the lines from file one by one and process them accordingly 
for line in file:
  if(ind==0):                              #First line is no. of routers. So store the value in N
    N = int(line)
  elif(ind==1):                            #Second line is list of routers.
    Routers  = line.strip('\n').split(' ') #We remove the new line character at the end and the white spaces and produce a list of the routers stored in 'Routers'
  elif line != "\n":                       #The rest of lines are stores in temporary list    
    Edges.append(line.strip('\n'))

  ind+=1
Routers.pop()
"""************************************************************************************************************************************************"""
# Initiate the Queues, Router tables of all routers with cost to self being 0 and to others a large no. M= 1000000
for i in range(len(Routers)):
  RouterId[Routers[i]] = i
  SQueue[Routers[i]] = queue.Queue()
  Neighbors[Routers[i]] = []


Table = []                                 #The list of router tables for all routers, where each entry contains the link cost and next hop
M = 10000000


for i in range(N):
  List = []
  for j in range(N):
    if(i==j):
      List.append([0,Routers[i]])
    else:
      List.append([M,"NA"])
  Table.append(List)
"""************************************************************************************************************************************************"""

#Process the edges, and fill the router tables accordingly
for e in Edges:
  Edge = e.split(' ')
  
  u = Edge[0]
  v = Edge[1]
  w = Edge[2]
  Neighbors[u].append(v)
  Neighbors[v].append(u)
    
  Table[RouterId[u]][RouterId[v]] = [int(w),v]
  Table[RouterId[v]][RouterId[u]] = [int(w),u]
  
  
"""************************************************************************************************************************************************"""
#Helper function to implement Link state routing protocol 
def Compute(router,iter):              
  
  R = RouterId[router]
  while iter<=N:                                #Run for the protoco for as many times as the no. of nodes.

    Cost ={}                                    # Cost is a dictionary which stores the routing tables of all the nodes in the network
    for i in Routers:
      Cost[i] ={}

    Cost[router] = Table[R]
    
    
    
    FwdTable = (Table[R],router)               #We forward the current router's tables to all the routers in the network

    for i in range(N):
      if(R!=i):
        SQueue[Routers[i]].put(FwdTable)
      
    
    
    for i in range(N-1):                      #We wait till we get response from all the remainig routers.Hence the loop is ran for N-1 times.
      response = SQueue[router].get()      
      Cost[response[1]] = response[0]
        
    
    
    
    

    Used = [False]*N
    Updated = [False]*N
    
    Used[R] = True
    Q = queue.Queue()                         #Queue contains all the current routers whose shortest path hasn't been calculated yet in other words those who haven't entered the Dijkstra Algorithm.
    Q.put(R)
    while not Q.empty():
    
      H = Q.get()                             #Dijkstra Algorithm
      
      Used[H]=True
      Next = -1
      MinCost = 100000000000
      for k in Neighbors[Routers[H]]:
        
        if not Used[RouterId[k]]:
          X = Table[R][H][0]+Cost[Routers[H]][RouterId[k]][0]
          if(Table[R][RouterId[k]][0]>(X)):
            Updated[RouterId[k]] =True
            Table[R][RouterId[k]][0] = X
            Table[R][RouterId[k]][1] = Routers[H]
          
          if(MinCost>Table[R][RouterId[k]][0]):
            Next = RouterId[k]
            MinCost = Table[R][RouterId[k]][0]

      if(Next!=-1):
        Q.put(Next)
        Used[Next]= True 

    
    
    Data =[]                                                                 #Make a list of lists containg the router table entries, inorder to print in tabulate format
    for j in range(N):
      F  = str(Table[R][j][0])
      if(F=="10000000"):
        F="INF"
      if Updated[j]:
        F = F+"*"

      item  = [Routers[j],F,Table[r][j][1]]
      Data.append(item)

    lock.acquire()                                                           #Since we are printing multiple lines, we need to make sure these are atomic i.e no other router prints in between. Hence we acquire a lock.
      
    print("---------------------------------------------------------------------")       
    print("Routing Table of " + str(router) + " after iteration " + str(iter) +" :")    
    print(tabulate(Data,headers= ["Router","Link Cost","Next Hop"],tablefmt="outline"))  
        
    print("")                                                                #Make the router wait for 2 secs before forwarding again
    time.sleep(1)                                    
    print("Router " +str(router) + " waiting for 1 sec")
    time.sleep(1)
    print("Router " +str(router) + " waiting for 2 secs")
    if(iter!=(N)):
      print("Forwarding Router table of Router "+str(router))
    else:
      print("Terminating routing protocol for router " + str(router))
    lock.release()                                                           #Release the lock
      
    iter+=1

"""************************************************************************************************************************************************"""

# Print initial routing tables for all routers 
for r in range(N):
  router  = Routers[r]
  print("---------------------------------------------------------------------")       
  print("Routing Table of " + str(router) + " intially"+" :")
  
  Data =[]
  for j in range(N):
    F  = str(Table[r][j][0])
    if(F=="10000000"):
      F="INF"
    item  = [Routers[j],F,Table[r][j][1]]
    Data.append(item)

  print(tabulate(Data,headers= ["Router","Link Cost","Next Hop"],tablefmt="outline"))  
      
  
#List to keep all threads created
Threads = []

for i in range(N):
  Thrd  = threading.Thread(target = Compute,args = (Routers[i],1,))          #Create a new thread with target function 'Compute' and for each router
  Threads.append(Thrd)

for i in range(N):
  Threads[i].start()                                                         #Begin execution of each thread

for i in range(N):  
  Threads[i].join()


  





