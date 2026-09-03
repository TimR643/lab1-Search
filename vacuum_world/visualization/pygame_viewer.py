"""
PyGame-based visualization for the vacuum world.
"""
import pygame
import sys
import time
from typing import Optional, Tuple
from ..world.world import World
from ..world.grid_pos import GridPos
from .colors import COLORS


class PygameViewer:    
    def __init__(self, 
                 world: World,
                 agent=None,
                 cell_size: int = 25,
                 window_width: int = 800,
                 window_height: int = 600):
        """Initialize the PyGame viewer.
        
        Args:
            world: The world to visualize
            agent: The agent to control (optional)
            cell_size: Size of each grid cell in pixels
            window_width: Window width
            window_height: Window height
        """
        self.world = world
        self.agent = agent
        self.cell_size = cell_size
        self.window_width = window_width
        self.window_height = window_height
        
        self.grid_width = world.width * cell_size
        self.grid_height = world.height * cell_size
        
        # Center the grid in the window
        self.grid_offset_x = (window_width - self.grid_width) // 2
        self.grid_offset_y = (window_height - self.grid_height) // 2
        
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Vacuum World")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)
        
        self.running = True
        self.paused = False
        self.show_expanded = True
        self.show_path = True
        
        # Initial simulation timing
        self.simulation_speed = 5  # Steps per second
        self.last_step_time = 0
    
    def grid_to_screen(self, grid_pos: GridPos) -> Tuple[int, int]:
        """Convert grid coordinates to screen coordinates.
        
        Args:
            grid_pos: Grid position
            
        Returns:
            Screen coordinates (x, y)
        """
        screen_x = self.grid_offset_x + grid_pos.x * self.cell_size
        screen_y = self.grid_offset_y + grid_pos.y * self.cell_size
        return (screen_x, screen_y)
    
    def draw_grid(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                pos = GridPos(x, y)
                screen_x, screen_y = self.grid_to_screen(pos)
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)
                
                # Draw cell background
                if self.world.maze.is_wall(pos):
                    pygame.draw.rect(self.screen, COLORS['wall'], rect)
                else:
                    pygame.draw.rect(self.screen, COLORS['floor'], rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, COLORS['border'], rect, 1)
    
    def draw_expanded_nodes(self):
        if not self.show_expanded:
            return
            
        for pos in self.world.expanded_nodes:
            if not self.world.maze.is_wall(pos):
                screen_x, screen_y = self.grid_to_screen(pos)
                rect = pygame.Rect(screen_x + 2, screen_y + 2, 
                                 self.cell_size - 4, self.cell_size - 4)
                pygame.draw.rect(self.screen, COLORS['expanded'], rect)
    
    def draw_path(self):
        if not self.show_path:
            return
            
        for pos in self.world.current_path:
            if not self.world.maze.is_wall(pos):
                screen_x, screen_y = self.grid_to_screen(pos)
                rect = pygame.Rect(screen_x + 4, screen_y + 4, 
                                 self.cell_size - 8, self.cell_size - 8)
                pygame.draw.rect(self.screen, COLORS['path'], rect)
    
    def draw_dirt(self):
        for dirt in self.world.get_all_uncleaned_dirt():
            screen_x, screen_y = self.grid_to_screen(dirt)
            center_x = screen_x + self.cell_size // 2
            center_y = screen_y + self.cell_size // 2
            radius = max(3, self.cell_size // 6)
            pygame.draw.circle(self.screen, COLORS['dirt'], (center_x, center_y), radius)
    
    def draw_agent(self):
        if self.world.agent:
            agent_pos = GridPos(self.world.agent.x, self.world.agent.y)
            screen_x, screen_y = self.grid_to_screen(agent_pos)
            center_x = screen_x + self.cell_size // 2
            center_y = screen_y + self.cell_size // 2
            radius = max(4, self.cell_size // 4)
            
            # Use different color if agent is on dirt
            dirt_at_pos = self.world.get_dirt_at_position(agent_pos)
            color = COLORS['agent_with_dirt'] if dirt_at_pos else COLORS['agent']
            
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
    
    def draw_ui(self):
        if self.world.agent:
            info_lines = [
                f"Agent: ({self.world.agent.x}, {self.world.agent.y})",
                f"Dirt collected: {self.world.agent.get_dirt_collected()}",
                f"Remaining dirt: {len(self.world.get_all_uncleaned_dirt())}",
                f"Status: {'COMPLETED' if self.world.is_terminated() else 'RUNNING'}"
            ]
            
        else:
            info_lines = ["No agent present"]
        
        y_offset = 10
        for line in info_lines:
            text_surface = self.font.render(line, True, COLORS['text'])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        # Controls
        controls = [
            "Controls:",
            "SPACE - Pause/Resume",
            "E - Toggle expanded nodes",
            "P - Toggle path display",
            "+/- - Speed up/down",
            "ESC - Exit"
        ]
        
        y_offset = self.window_height - len(controls) * 20 - 10
        for line in controls:
            text_surface = self.small_font.render(line, True, COLORS['text'])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 16
        
        # Draw mode indicators
        mode_text = []
        if self.paused:
            mode_text.append("PAUSED")
        mode_text.append(f"Speed: {self.simulation_speed}/sec")
        
        for i, text in enumerate(mode_text):
            surface = self.font.render(text, True, COLORS['text'])
            self.screen.blit(surface, (self.window_width - 200, 10 + i * 25))
    
    def handle_events(self):
        """Handle PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                elif event.key == pygame.K_e:
                    self.show_expanded = not self.show_expanded

                elif event.key == pygame.K_p:
                    self.show_path = not self.show_path

                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # (Quick fix for some non-standard keyboard layouts)
                    self.simulation_speed = min(20, self.simulation_speed + 1)
                    print(f"Simulation speed: {self.simulation_speed} steps/sec")

                elif event.key == pygame.K_MINUS:
                    self.simulation_speed = max(1, self.simulation_speed - 1)
                    print(f"Simulation speed: {self.simulation_speed} steps/sec")
    
    
    def update(self):
        """Update the visualization (called by world when it changes)."""
        # TODO: Find out where this is used
        # This method is called by the world when it changes
        # We don't need to do anything here as we redraw everything each frame
        pass
    
    def render(self):
        """Render one frame of the visualization."""
        # Clear screen
        self.screen.fill(COLORS['background'])
        
        # Draw world elements
        self.draw_grid()
        self.draw_expanded_nodes()
        self.draw_path()
        self.draw_dirt()
        self.draw_agent()
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self, target_fps: int = 30):
        """Run the visualization main loop.
        
        Args:
            target_fps: Target frames per second
        """
        while self.running:
            self.handle_events()
            
            if not self.paused and self.agent:
                current_time = time.time()
                step_interval = 1.0 / self.simulation_speed
                
                if current_time - self.last_step_time >= step_interval:
                    if not self.world.is_terminated():
                        self.agent.step(self.world)
                        self.last_step_time = current_time
            
            self.render()
            self.clock.tick(target_fps)
        
        pygame.quit()
        sys.exit()