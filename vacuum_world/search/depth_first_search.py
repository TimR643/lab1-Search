from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch


class DepthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return []
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return []