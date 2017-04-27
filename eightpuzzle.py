#Jasmine Farley
import heapq #imported for priority queue

class FIFO_Queue():
    'Defines a first in, first out queue.'
    def __init__(self): #Constructor
        'Takes a list of items/objects'
        self.items = []

    def enqueue(self, item):
        'Adds an item to the queue'
        self.items.append(item)

    def pop(self):
        'Takes the first item in the queue out of the queue'
        return self.items.pop(0)

    def size(self):
        'Returns an integer that represents the length of the queue'
        return len(self.items)
    
    def isEmpty(self):
        'Returns a boolean value to determine if the queue is empty '
        return self.items == []
        
    def __eq__(self, other):
        'Returns a boolean value to determine if the queue contains the same items as another'
        return self.items == other.items
    
    def __contains__(self, item):
        'Checks if an item is in the queue.'
        for x in self.items:
            if item == x:
                return True
            else:
                return False

class LIFO_Queue():
    'Defines a last in, first out queue.'
    
    def __init__(self): #Constructor
        'Takes a list of items/objects'
        self.items = []

    def enqueue(self, item):
        'Adds an item to the queue'
        self.items.append(item)

    def pop(self):
        'Returns the item that was last inserted'
        return self.items.pop()

    def size(self):
        'Returns how many items are in the queue'
        return len(self.items)
    
    def isEmpty(self):
        'Boolean value to determine if a queue is empty'
        return self.items == []
        
    def __eq__(self, other):
        'Returns a boolean value to determine if the queue contains the same items as another'
        return self.items == other.items
    
    def __contains__(self, item):
        'Checks if an item is in the queue.'
        for x in self.items:
            if item == x:
                return True
            else:
                return False    

class Priority_Queue():
    'Defines a Priority Queue'
    
    def __init__(self): #constructor
        'Adds items to a queue accorind to priority'
        self.items = []
        
    def enqueue (self, priority, node ):
        'Adds a new item to to the queue'
        heapq.heappush(self.items, (priority, node ))
    
    def update(self, priority, node ):
        'Updates the priority of an existing item if priority is smaller'
        for item in self.items:
            if node.state == item[1].state:
                if priority < item[0]: #checks if the priority is smaller 
                    self.items.pop(self.items.index(item))
                    self.enqueue(priority, node)
                else:
                    pass
            
    def __iter__(self):
        'Adds the ability to iterate through the queue'
        return iter(self.items)
    
    def pop(self):
        'Returns the item with the lowest priority'
        return heapq.heappop(self.items)[1]
    
    def size(self):
        'Returns the number of items in teh queue'
        return len(self.items)
 
    def isEmpty(self):
        'Boolean value to determine if the queue is empty'
        return self.items == []
    
    def found(self, node):
        'Finds and returns a specific node from the queue'
        return node in (item[1] for item in self.items)

class Node:
    'Defines a node'
    
    def __init__(self, state, parent, action, cost, depth): #constuctor
        'Defines what a Node object contains'
        self.state = state 
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        
    def get_successors(self):
        "Returns all posible children and computes it's cost and depth"
        blank_space = self.state.index(0) #returns the index of the zeron in the array
        children = [] #creates an array to hold it's sucessors/ children
        cost = self.cost #sets the cost to the cost of the parent's
        depth = self.depth #sets the depth to the dept of the parents
        
        if blank_space > 2:  # if the zero's index is greater than 2 it's able to move up
            child = self.state[:] # makes a copy of the list 
            depth += 1 # adds one to the depth because it is now down a level
            #switches places with the the number that is above it:
            child[blank_space], child[blank_space-3] = child[blank_space-3], child[blank_space]
            cost = cost + child[blank_space] # increases the cost by the number that was in the space
            children.append(Node(child, self, "UP", cost, depth)) #adds the child to the successors array
        
        if blank_space not in [0 , 3 ,6] : #if the zero's index is not one of these numbers it's able to move left 
            child = self.state[:]
            depth += 1
            cost += child[blank_space-1]
            child[blank_space], child[blank_space-1] = child[blank_space-1], child[blank_space]
            children.append(Node(child, self, "LEFT", cost, depth))
       
        if blank_space not in [2, 5, 8] : #if the zero's index is not one of these numbers it's able to move right 
            child = self.state[:]
            depth += 1
            cost = cost + child[blank_space+1]
            child[blank_space], child[blank_space+1] = child[blank_space+1], child[blank_space]
            children.append(Node(child, self, "RIGHT", cost, depth))
        
        if blank_space < 6: # if the zero's index is less than six it is able to move down
            child = self.state[:]
            depth += 1
            cost = cost + child[blank_space+3]
            child[blank_space], child[blank_space+3] = child[blank_space+3], child[blank_space]
            children.append(Node(child, self, "DOWN", cost,  depth))

        return children

    def __str__(self):
        'Returns the string as a list'
        return ("[ %s, %s, %s, %s, %s ]" % (self.state, self.parent, self.action, self.cost, self.depth))
    
    def __eq__(self, other):
        "Checks if a Node's state is the same as another's" 
        return self.state == other.state
    
def heuristic (state, goal):
    "Determines the number of misplaced tiles"
    num = 0
    for i in range(len(state)):
        if state[i] != goal[i]:
            num += 1
    return num

def bfs(initial): #takes a Node's state
    "Breadth first search for puzzle solution"
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0) #the goal Node/State
    node = Node(initial, None, None, 0, 0) #turns the state given into a Node
    frontier = FIFO_Queue() # initializes an empty FIFO queue
    explored = [] #initialized an empty list
    time = 0
    if node.state == goal.state: #if the given state is the solution it returns
        print( "Solved! Total Cost: " + str(node.cost))
        return
    frontier.enqueue(node) # if not it add the item to the queue
    while frontier.isEmpty() == False: # while the queue is not empty
        time +=1
        current_node = frontier.pop() #pop off the first node
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        explored.append(current_node.state) #add the state to the explored list
        children = current_node.get_successors() #get it's children 
        for child in children: #loop through the children 
            if  (child not in frontier) and (child.state not in explored): #if we have not seen this child state
                if (child.state == goal.state): #check if it's the solution if it is return
                    print ("Node Cost: "+ str(child.cost) + " " + str(child.state))
                    print( "Solved! Total Cost: " +  str (child.cost ))
                    print(str(time) + " " + str(child.depth))
                    return
                frontier.enqueue(child) #else add the child to the queue
    return "failure"

def dfs(initial):
    "Depth first search for puzzle solution"
    #almost the same as BFS except the order that it is popped of the queue is different 
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0)
    node = Node(initial, None, None, 0, 0)
    time = 0
    frontier = LIFO_Queue() #last in first out queue is initialized
    explored = []
    if node.state == goal.state:
        print( "Solved! Total Cost: " + str(node.cost))
        return
    frontier.enqueue(node)
    while frontier.isEmpty() == False:
        time +=1
        current_node = frontier.pop()
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        explored.append(current_node.state)
        children = current_node.get_successors()
        for child in children:
            if  (child not in frontier) and (child.state not in explored):
                if child.state == goal.state:
                    print ("Node Cost: "+ str(child.cost) + " " + str(child.state))
                    print( "Solved! Total Cost: " + str(child.cost))
                    print(str(time) + " " + str(child.depth))
                    return
                frontier.enqueue(child)
    return "failure"

def uniform_cost(initial):
    "Uniform Cost to find puzzle solution"
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0)
    node = Node(initial, None, None, 0, 0)
    frontier = Priority_Queue() #uses a priority queue 
    frontier.enqueue(node.cost, node) #orderd by the Node's cost
    explored = [] #empty set to keep track of explored states
    time = 0
    while frontier.isEmpty()==False: #while the queue is not empty
        time +=1
        current_node = frontier.pop() #pop of the Node with the lowest cost
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        if current_node.state == goal.state: #if goal state is found return
            print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
            print( "Solved! Total Cost: " + str(current_node.cost))
            print(str(time) + " " + str(current_node.depth))
            return
        explored.append(current_node.state) # add the state to the explored 
        children = current_node.get_successors() #gets children
        for child in children:
            if  (frontier.found(child)==False) and (child.state not in explored):  #if it is a new node it adds it to the queue
                 frontier.enqueue(child.cost, child)
            elif frontier.found(child)==True: #if the node is already in the queue 
                frontier.update(child.cost, child) #it checks if the the priority using the update function 
    return 'failure'

def bestfs(initial):
    "Uses best first search to find puzzle solution"
    
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0)
    node = Node(initial, None, None, 0, 0)
    wrongpositions = heuristic(initial, goal.state) #the number of numbers not in their correct index
    frontier = Priority_Queue()
    frontier.enqueue(wrongpositions, node) # a priority queue where the priority is heuristic of the state
    explored = []
    time = 0
    while frontier.isEmpty()==False:
        time +=1
        current_node = frontier.pop() #pops off the node with the less amount of misplaced tiles
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        if current_node.state == goal.state:
            print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
            print( "Solved! Total Cost: " + str(current_node.cost))
            print(str(time) + " " + str(current_node.depth))
            return
        explored.append(current_node.state)
        children = current_node.get_successors() #gets the successors
        for child in children:
            wrongpositions = heuristic(child.state, goal.state) #gets the number of misplaces tiles for the child
            if  (frontier.found(child)==False) and (child.state not in explored): #if it has not been sene 
                 frontier.enqueue(wrongpositions, child) #add it to the queue 
            elif frontier.found(child)==True: #if it is in the queue
                frontier.update(wrongpositions, child) #check to see if the heuristic is smaller
    return 'failure'

def a_one(initial):
    "A* to find the solution to the puzzle using misplaced tiles as heuristic"
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0)
    node = Node(initial, None, None, 0, 0)
    explored = []
    wrongpositions = heuristic(initial, goal.state) # gets the number of misplaced tiles 
    frontier = Priority_Queue()
    frontier.enqueue((wrongpositions+node.cost), node) #adds a node to the queue according to the sum of the misplaced tiles and cost
    time = 0
    while(frontier.isEmpty()==False):
        time += 1
        current_node = frontier.pop()
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        if(current_node.state == goal.state):
            print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
            print( "Solved! Total Cost: " + str(current_node.cost))
            print(str(time) + " " + str(current_node.depth))
            return
        children = current_node.get_successors()
        wrongpositions = heuristic(current_node.state, goal.state)
        for child in children: #loops through successors
            if(child.state == goal.state):
                print ("Node Cost: "+ str(child.cost) + " " + str(child.state))
                print( "Solved! Total Cost: " + str(child.cost))
                print(str(time) + " " + str(child.depth))
                return
            current_node = child #sets the child as the current node
            wrongpositions2 = heuristic(child.state, goal.state)
            if(frontier.found(child) == True) and (wrongpositions == wrongpositions2) :
                continue #skips the node
            elif (child.state in explored) and (wrongpositions == wrongpositions2):
                continue #skips the node
            else:
                frontier.enqueue((wrongpositions2+child.cost), child) #adds a node to the queue according to the sum of the misplaced tiles and cost
        explored.append(current_node.state)
    return "failure"
                   
                   
def a_two(initial):
    "A* using manhattan distance as heurstic"
    #same as a_one but uses manahttan distance as heurstic 
    goal = Node ([1,2,3,8,0,4,7,6,5], None, None, 0, 0)
    node = Node(initial, None, None, 0, 0)
    explored = []
    wrongpositions = manhattan(node, goal.state)
    frontier = Priority_Queue()
    frontier.enqueue(wrongpositions, node)
    time = 0
    while(frontier.isEmpty()==False):
        time +=1
        current_node = frontier.pop()
        print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state))
        if(current_node.state == goal.state):
            print ("Node Cost: "+ str(current_node.cost) + " " + str(current_node.state)) 
            print( "Solved! Total Cost: " + str(current_node.cost))
            print(str(time) + " " + current_node.depth)
            return
        children = current_node.get_successors()
        wrongpositions = manhattan(current_node, goal.state)
        for child in children:
            if(child.state == goal.state):
                print ("Node Cost: "+ str(child.cost) + " " + str(child.state))
                print( "Solved! Total Cost: " + str(child.cost))
                print(str(time) + " " + str(child.depth))
                return
            current_node = child.parent
            wrongpositions2 = manhattan(child, goal.state)
            if(frontier.found(child) == True) and (wrongpositions == wrongpositions2) :
                continue #skips the node
            elif (child.state in explored) and (wrongpositions == wrongpositions2):
                continue #skips the node
            else:
                frontier.enqueue(wrongpositions2, child)
        explored.append(current_node.state)
    return "failure"

def manhattan(node, goal_state):
    "Calculates manhattan distance"
    state = node.state
    misplaced = 0
    manhattan = 0
    for i in range(len(state)):
        if state[i] != goal_state[i]:
            misplaced += 1
    for i in range(len(state)):
        x = abs((state.index(i)//3) - (goal_state.index(i)//3))
        y = abs((state.index(i)%3) - (goal_state.index(i)%3))
        manhattan = manhattan + (x + y)
    if (manhattan>misplaced):
        return (node.cost +manhattan) #stores the cost sum and the manahattan distances
    else:
        return (node.cost +misplaced)  #stores the sum of the misplaced tiles and cost
   
def main():
    print("****EASY*****")
    easy = [1,3,4,8,6,2,7,0,5]
    print (easy)
    print("*******A2**********")
    a_two(easy)
    print("*******A1**********")
    a_one(easy)
    print("*******BEST FS**********")
    bestfs(easy)
    print("*******UNIFORM COST**********")
    uniform_cost(easy)
    print("*******BFS**********")
    bfs(easy)
    print("*******DFS**********")
    dfs (easy)
    medium = [2, 8, 1, 0, 4, 3, 7, 6, 5]
    print("*****MEDIUM*******")
    print (medium)
    print("*******A2**********")
    a_two(medium)
    print("*******BEST FS**********")
    bestfs(medium)
    print("*******UNIFORM COST**********")
    uniform_cost(medium)
    print("*******BFS**********")
    bfs(medium)
    print("*******DFS**********")
    dfs (medium)
    print("*******A1**********")
    a_one(medium)
    hard = [5, 6, 7, 4, 0, 8, 3, 2, 1]
    print("*******BEST FS**********")
    bestfs(hard)
    # print ("******HARD*****")
    # print (hard)
    # print("*******A2**********")
    # a_two(hard)
    # print("*******A1**********")
    # a_one(hard)
    # print("*******UNIFORM COST**********")
    # uniform_cost(hard)
    # print("*******BFS**********")
    # bfs(hard)
    # print("*******DFS**********")
    # dfs (hard)
    
#    print(Node([1,3,4,8,6,2,7,0,5], None, None, 0, 0))

if __name__ == "__main__": main()
