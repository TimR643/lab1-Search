from .grid_pos import GridPos


class VacuumAgent(GridPos):
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.dirt_collected = 0
    
    def move_to(self, new_pos: GridPos):
        self.x = new_pos.x
        self.y = new_pos.y
    
    def collect_dirt(self):
        self.dirt_collected += 1
    
    def get_dirt_collected(self) -> int:
        return self.dirt_collected
    
    def at_position(self, pos: GridPos) -> bool:
        return self.x == pos.x and self.y == pos.y
    
    def __str__(self) -> str:
        return f"Agent({self.x}, {self.y}) - collected: {self.dirt_collected}"
    
    def __repr__(self) -> str:
        return f"VacuumAgent({self.x}, {self.y}, dirt_collected={self.dirt_collected})"