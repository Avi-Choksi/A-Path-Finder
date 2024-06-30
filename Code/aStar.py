import math

# Create a list of cities with the correct children and weights
def populateCities(nodes, graph):
    citylist = []
    for i in range(len(graph)):
        place = Node(nodes[i][0], [], nodes[i][-2:], 0, 0)
        citylist.append(place)
    populateCitiesHelper(nodes, graph, citylist, 0, nodes [len(graph) - 1][-2:])
    
    # Set the heuristic of each city
    for node in citylist:
        if len(node.getChildren()) == 0:
            hValue = float("inf")
        else:
            minCost = node.getChildren()[0][0]
            minNode = node
            for child in node.getChildren():
                if child[0] < minCost:
                    minCost = child[0]
                    minNode = child[1]
            distance = minNode.getDistance(node.coord)
            if distance == 0:
                hValue = minCost
            else:
                hValue = minCost/distance
        node.h = hValue
    return citylist

# Recursive helper to add children to each city    
def populateCitiesHelper(cities, graph, citylist, current, end):
    currents = graph[current]
    i = 0
    for weight in currents:
        # Only add if there is a weight listed and the start city should never be a child
        if int(weight) > 0 and i != 0:
            citylist[current].addChild([float(weight), citylist[i]])
        i += 1
    # Iterate until every row in weight matrix is accounted for
    if current < len(graph) - 1:
        populateCitiesHelper(cities, graph, citylist, current + 1, end)
    return

# A* Search Algorithm
def aSearch(start, citylist, end):
    backTrace = dict()
    found = []
    cost = dict()
    cost[start[0]] = 0
    queue = PriorityQueue()
    queue.insert(start)
    while queue:
        # Get the lowest cost node that hasn't been expanded already
        current = queue.delete()
        if current[0] in found:
            continue

        # Check if the current node is the goal node
        if current[0].getNode() == citylist[end[0]].getNode():
            # Backtrack to find the final path and return it
            path = [current]
            while current[0] != start[0]:
                current = backTrace[current[0]]
                path.append(current)
            return list(reversed(path)), len(found)

        # Add the node to the list of expanded nodes    
        found.append(current[0])

        # Add all children to the priority queue based on cost
        for next in current[0].getChildren():
            prevCost = current[1]
            queue.insert(
                [next[1], next[0] + prevCost],
                priority = next[0] + prevCost + (next[1].h)
            )

            # If the found child has not been found or the cost
            # of getting to the child is less then what was found,
            # change it's parent in the backtrace and update cost
            if (next[1] not in cost
                or next[0] + current[1] < cost[next[1]]):
                cost[next[1]] = next[0] + current[1]
                backTrace[next[1]] = [current[0], next[0] + current[1]]
    
    # Return none if no path is found
    return None

# Node class to store board state data
class Node:
    def __init__(self, node, child, coord, f, h):
        self.node = node
        self.child = child
        self.coord = coord[1]
        self.f = f
        self.h = h
    def addChild(self, child):
        self.child.append(child)
    def getChildren(self):
        return self.child
    def getNode(self):
        return self.node
    def getDistance(self, end):
        distance1 = abs(float(end[0]) - float(self.coord[0]))
        distance2 = abs(float(end[1]) - float(self.coord[1]))
        return math.sqrt(pow(distance1, 2) + pow(distance2, 2))

# Queue that gets elements based on a pre-set priority
class PriorityQueue():
    def __init__(self):
        self.queue = []
        self.size = 0
 
    def getLength(self):
        return self.size

    def insert(self, current, priority = 0):
        self.queue.append([current, priority])
        self.size += 1
 
    # Deletes and returns the object that has the lowest priority number in the queue
    def delete(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i][1] < self.queue[min][1]:
                min = i
        if len(self.queue) == 0:
            return None
        found = self.queue[min][0]
        self.size -= 1
        del self.queue[min]
        return found