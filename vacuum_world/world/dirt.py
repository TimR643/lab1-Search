from .grid_pos import GridPos


class Dirt(GridPos):
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.cleaned = False
    
    def clean(self):
        self.cleaned = True
    
    def is_cleaned(self) -> bool:
        return self.cleaned
    
    def __str__(self) -> str:
        status = "cleaned" if self.cleaned else "dirty"
        return f"Dirt({self.x}, {self.y}) - {status}"
    
    def __repr__(self) -> str:
        return f"Dirt({self.x}, {self.y}, cleaned={self.cleaned})"