from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

class Stack:
    def __init__(self):
        self.lst = []
        
    def push(self,x):
        self.lst.append(x)
        
    def pop(self):
        return self.lst.pop()
    
    def isEmpty(self):
        return len(self.lst) == 0
    
    def peek(self):
        return self.lst[-1]
   
def main():
    def goto(t,node,maze):
        row,col = node
        x = squareWidth * col + squareWidth/2.0
        y = squareHeight * row + squareHeight/2.0
        t.goto(x,y)
    
    def trace(path,turtle, maze, color):
        turtle.color(color)
        turtle.pendown()
        turtle.width(10)
        
        for node in path:
            goto(turtle, node, maze)
            
        turtle.penup()
        
    root = tkinter.Tk()
    root.title("Hill Climbing Maze")
    cv = ScrolledCanvas(root,600,600,600,600)
    cv.pack(side = tkinter.LEFT)
    t = RawTurtle(cv)
    screen = t.getscreen()
    screen.bgcolor("green")
    t.ht()
    screen.setworldcoordinates(0,0,600,600)
    
    def drawSquare(row,col,color):
        t.penup()
        t.color(color)
        t.goto(col*squareWidth, row*squareHeight)
        t.setheading(0)
        t.begin_fill()
        t.forward(squareWidth)
        t.left(90)
        t.forward(squareHeight)
        t.left(90)
        t.forward(squareWidth)
        t.left(90)
        t.forward(squareHeight)
        t.end_fill()
    
    
    maze = []
    file = open("maze2.txt", "r")
    rows = int(file.readline())
    cols = int(file.readline())
    squareWidth = 600.0 / cols
    squareHeight = 600.0 / rows
    for line in file:
        maze.append((line+"                                                            ")[:cols])
        
    screen.tracer(0)
    
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "*":
                drawSquare(row, col, "blue")
    
        
    screen.tracer(1)
    screen.update()
    
    for c in range(cols):
        if maze[rows-1][c] == " ":
            endCol = c
        
    def mouseHandler(x,y):
        for c in range(cols):
            if maze[0][c] == " ":
                startCol = c
        screen.update()
        print(x,y)
        path = hillclimbing((0,startCol),goal,[])
        trace(path, t, maze, "purple")
        
        
    def adjacent(row,col):
        adjList = []
        if col < cols-1:
            if maze[row][col+1] == " ":
                adjList.append((row,col+1))
        if col > 0:
            if maze[row][col-1] == " ":
                adjList.append((row,col-1))
        if row < rows:
            if maze[row+1][col] == " ":
                adjList.append((row+1,col))
        if row > 0:
            if maze[row-1][col] == " ":
                adjList.append((row-1,col))
        return adjList
    
    
    
    def hillclimbing(current,goal,visited): 
        stack = Stack()
        stack.push([current])
        visited = []

        t.penup()
        t.st()
        goto(t,current,maze)
        
        while not stack.isEmpty():
            currentPath = stack.pop()
            currentNode = currentPath[0]
            visited.append(currentNode)
            t.st()
            goto(t, currentNode, maze)
            
        
                
            if goal(currentNode):
                print("found the goal")
                return currentPath
            row,col = currentNode
            adjList = adjacent(row,col)
            adjList = [x for x in adjList if x not in visited]
            nodelist = []
            for d in adjList:
                n = Node(d[0],d[1])
                nodelist.append(n)
            print("Before sort:")
            for i in nodelist:
                print(i.getRow(),i.getCol())
            nodelist.sort()
            print("After sort:")
            for i in nodelist:
                print(i.getRow(),i.getCol())
                
            if len(nodelist) == 0:
                # backtrack
                if not stack.isEmpty():
                    lastPath = stack.peek()
                    pathDiff = currentPath[0:(len(currentPath)-len(lastPath))+1]
                    trace(pathDiff,t,maze, "red")
                    
            else:
                for adjNode in nodelist:
                    stack.push([(adjNode.getRow(),adjNode.getCol())]+currentPath)
                
        # did not find a path
        return None

    def goal(node):
        row,col = node
        return row == rows-1
    
    def manhattan(otherNode,goalNode):
        manhattanDist = abs(goalNode.getRow() - otherNode.getRow()) + abs(goalNode.getCol() - otherNode.getCol())
        return manhattanDist
    
    
    class Node:
        def __init__(self,row,col):
            self.row = row
            self.col = col
            
        def __lt__(self,other):
            goal = Node(rows-1,endCol)
            return manhattan(self,goal) > manhattan(other,goal)
        
        def getRow(self):
            return self.row
        
        def getCol(self):
            return self.col
        
        
  

    
    screen.listen()
    screen.onclick(mouseHandler)
    tkinter.mainloop()
    


            
if __name__ == "__main__":
    main()