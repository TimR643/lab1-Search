from collections import deque
from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch


# Goal is to implement the breadth-first algorithm, which walks through the search tree level by level, 
# exploring all nodes at the present depth before moving on to the nodes at the next depth level. This is achieved using a queue (FIFO) data structure for the frontier.
class BreadthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = [] #reset the path to empty list
        self.frontier = deque() #empty the queue
        self.explored = [] #empty the explored list
        
        initial_state = problem.get_initial_state() #finding initial state
        root = SearchNode(state=initial_state) #create the root of the search tree with this initial state
        self.frontier.append(root) 
        frontier_states = {root.get_state()}
        explored_states = set()        
        
        while self.frontier: #do while there are still nodes in the frontier
            node = self.frontier.popleft() # pop the first node from the frontier -> FIFO
            frontier_states.remove(node.get_state()) #  remove the state of this node from the frontier states set
            
            if problem.is_goal_state(node.get_state()): #check for goal state
                self.path = node.get_path_from_root()
                return self.path #if so, return return the path from root to this node   
                
            self.explored.append(node) #mark node as explored
            explored_states.add(node.get_state()) # add the state of this node to the explored states set

            if node.get_cost() >= self.max_depth:
                continue

            for state in problem.get_successors(node.get_state()): #get reachable positions/nodes
                if state in explored_states or state in frontier_states:
                    continue
                child = SearchNode(state, node, cost=node.get_cost() + 1) #create a new search node for this state, with the current node as its parent and incrementing the cost
                self.frontier.append(child) #appending the new node to the queue
                frontier_states.add(state)

        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)