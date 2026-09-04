"""
A* Search implementation.
A* expands the node of the frontier with the lowest f(n) = g(n) + h(n), where
g(n) is the cost of the path from the initial state to n, and h(n) is a
heuristic estimate of the remaining cost from n to the goal.
"""
import heapq
from typing import Callable, Dict, List, Optional, Set
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


# ---------------------------------------------------------------------------
# Heuristic functions
#
# In this domain the agent only moves North / South / East / West, and every
# move costs 1. A heuristic is admissible if it never overestimates the cost of
# an optimal path from a state to the goal.
# ---------------------------------------------------------------------------

def manhattan_heuristic(state: GridPos, goal: GridPos) -> float:
    """
    Manhattan distance |dx| + |dy|.

    Admissible: every move changes exactly one coordinate by exactly 1, so any
    path to the goal needs at least |dx| moves along x and |dy| moves along y.
    Walls can only make the real path longer, never shorter.
    It is also consistent, since one move changes the estimate by at most 1,
    which is exactly the cost of that move.
    """
    return float(abs(state.x - goal.x) + abs(state.y - goal.y))


def euclidean_heuristic(state: GridPos, goal: GridPos) -> float:
    """
    Straight line distance sqrt(dx^2 + dy^2).

    Admissible, because it is never larger than the Manhattan distance, which
    is itself a lower bound on the real cost. It is however a weaker estimate:
    it is dominated by the Manhattan heuristic, so A* expands more nodes with it.
    """
    return state.distance_euclidean(goal)


def null_heuristic(state: GridPos, goal: GridPos) -> float:
    """
    Constant zero heuristic.

    Trivially admissible. With it, f(n) = g(n) and A* degenerates into Uniform
    Cost Search. It is provided as a baseline to measure what the informed
    heuristics actually save.
    """
    return 0.0


HEURISTICS: Dict[str, Callable[[GridPos, GridPos], float]] = {
    "manhattan": manhattan_heuristic,
    "euclidean": euclidean_heuristic,
    "null": null_heuristic,
}


class AStarNode(SearchNode):
    """
    A search node that also stores the heuristic estimate of its state.

    A* needs more information than blind search: on top of the path cost g
    inherited from SearchNode, the node carries h, and orders itself by
    f = g + h so it can be stored directly in a heapq priority queue.
    """

    def __init__(self, state: GridPos, parent: Optional['AStarNode'] = None,
                 action: Optional[str] = None, cost: float = 0.0, heuristic: float = 0.0):
        """Initialize an A* node.

        Args:
            state: The state (grid position) this node represents
            parent: The parent node (None for root)
            action: The action taken to reach this state (unused, kept for compatibility)
            cost: The path cost g(n) to reach this state
            heuristic: The heuristic estimate h(n) of the cost left to the goal
        """
        super().__init__(state, parent, action, cost)
        self.heuristic = heuristic

    def get_heuristic(self) -> float:
        """Get the heuristic estimate h(n) of this node."""
        return self.heuristic

    def get_evaluation(self) -> float:
        """Get the evaluation function f(n) = g(n) + h(n) of this node."""
        return self.cost + self.heuristic

    def __lt__(self, other) -> bool:
        """
        Order nodes by f(n), so that heapq always pops the most promising one.

        Ties on f are broken in favour of the smaller h, i.e. the node that is
        estimated to be closer to the goal. This drives the search towards the
        goal instead of spreading over the many equally rated nodes of a grid.
        """
        if not isinstance(other, AStarNode):
            return NotImplemented
        if self.get_evaluation() != other.get_evaluation():
            return self.get_evaluation() < other.get_evaluation()
        return self.heuristic < other.heuristic

    def __str__(self) -> str:
        """String representation."""
        return (f"AStarNode(state={self.state}, g={self.cost}, "
                f"h={self.heuristic}, f={self.get_evaluation()})")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"AStarNode(state={self.state}, "
                f"parent={self.parent.state if self.parent else None}, "
                f"g={self.cost}, h={self.heuristic}, f={self.get_evaluation()})")


class AStarSearch(BaseSearch):

    def __init__(self, heuristic: str = "manhattan"):
        """Initialize A* search.

        Args:
            heuristic: Name of the heuristic to use ("manhattan", "euclidean" or "null")
        """
        super().__init__()
        if heuristic not in HEURISTICS:
            raise ValueError(f"Unknown heuristic {heuristic}, expected one of {list(HEURISTICS)}")
        self.heuristic_name = heuristic
        self.heuristic_function = HEURISTICS[heuristic]

        # Priority queue of AStarNode, ordered by f(n), managed with heapq
        self.frontier: List[AStarNode] = []
        # AStarNode objects already expanded, in expansion order
        self.explored: List[AStarNode] = []
        # GridPos of the expanded nodes, for O(1) lookups
        self.explored_states: Set[GridPos] = set()
        # Best known path cost g for every state reached so far
        self.best_cost: Dict[GridPos, float] = {}

    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform an A* search to find a path to goal.

        With an admissible heuristic and unit action costs, the first goal node
        popped from the priority queue is on an optimal path.
        """
        self.path = []
        self.frontier = []
        self.explored = []
        self.explored_states = set()
        self.best_cost = {}

        goal_state = problem.goal_state
        initial_state = problem.get_initial_state()

        root = AStarNode(initial_state, None, None, 0.0,
                         self.heuristic_function(initial_state, goal_state))
        heapq.heappush(self.frontier, root)
        self.best_cost[initial_state] = 0.0

        while self.frontier:
            # Pop the node with the lowest f(n) = g(n) + h(n)
            current_node = heapq.heappop(self.frontier)
            current_state = current_node.get_state()

            # A state can sit in the heap several times, only expand the best entry
            if current_state in self.explored_states:
                continue

            self.explored_states.add(current_state)
            self.explored.append(current_node)

            # Goal test at expansion time: testing at generation time would break
            # optimality, since a cheaper path to the goal may still be pending
            if problem.is_goal_state(current_state):
                self.path = current_node.get_path_from_root()
                return self.path

            if current_node.get_cost() >= self.max_depth:
                continue

            for successor in problem.get_successors(current_state):
                if successor in self.explored_states:
                    continue

                new_cost = current_node.get_cost() + 1

                # Keep only the cheapest path found so far to that state
                if successor in self.best_cost and self.best_cost[successor] <= new_cost:
                    continue

                self.best_cost[successor] = new_cost
                child = AStarNode(successor, current_node, None, new_cost,
                                  self.heuristic_function(successor, goal_state))
                heapq.heappush(self.frontier, child)

        # The frontier is empty: the goal is unreachable
        return []


    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)

    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)
