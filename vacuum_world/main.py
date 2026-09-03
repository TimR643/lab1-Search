"""
Main entry point for the Vacuum World Search Lab.
"""
import argparse
import sys
from rich import print
from .world.world import World
from .world.maze import MazeType
from .agent.vacuum_agent import IntelligentVacuumAgent, SearchMethod
from .visualization.pygame_viewer import PygameViewer


def parse_arguments():
    parser = argparse.ArgumentParser(description="Vacuum World - AI Search Lab")
    
    parser.add_argument('--size', type=int, default=20,
                       help='Size of the maze (default: 20)')
    parser.add_argument('--dirt', type=int, default=10,
                       help='Number of dirt particles (default: 10)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducible worlds')    
    parser.add_argument('--maze', choices=['default', 'simple', 'office', 'caves'],
                       default='default', help='Maze type to use (default: default)')
    parser.add_argument('--search', choices=['bfs', 'dfs', 'astar', 'random'],
                       default='bfs', help='Search method to use (default: bfs)')
    parser.add_argument('--no-gui', action='store_true',
                       help='Run without graphical interface')
    parser.add_argument('--cell-size', type=int, default=25,
                       help='Size of each grid cell in pixels (default: 25)')
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    maze_types = {
        'default': MazeType.MAZE_LABYRINTH,
        'simple': MazeType.MAZE_ONLY_BORDER,
        'office': MazeType.MAZE_OFFICE,
        'caves': MazeType.MAZE_CAVES
    }
    maze_type = maze_types[args.maze]
    
    world = World(
        width=args.size,
        height=args.size,
        num_dirt=args.dirt,
        maze_type=maze_type,
        seed=args.seed
    )
    
    print(f"[bold]Created world: [/bold][white] {args.size}x{args.size}, {args.dirt} dirt particles")
    print(f"[bold]Maze type: [/bold][white] {maze_type.value}")
    print(f"[bold]Random seed: [/bold][white]{world.seed}")
    
    agent = IntelligentVacuumAgent(world)
    
    search_methods = {
        'bfs': SearchMethod.BREADTH_FIRST_SEARCH,
        'dfs': SearchMethod.DEPTH_FIRST_SEARCH,
        'astar': SearchMethod.A_STAR_SEARCH,
        'random': SearchMethod.RANDOM_SEARCH
    }
    agent.set_search_method(search_methods[args.search])
    
    if args.no_gui:
        run_without_gui(world, agent)
    else:
        run_with_gui(world, agent, args.cell_size)


def run_without_gui(world: World, agent: IntelligentVacuumAgent):
    print("Running without GUI...")
    print("Initial state:", world.get_state_info())
    
    max_steps = 1000
    step_count = 0
    
    while not world.is_terminated() and step_count < max_steps:
        agent.step(world)
        step_count += 1
        
        if step_count % 100 == 0:
            print(f"Step {step_count}: {world.get_state_info()}")
    
    print(f"\nSimulation completed after {step_count} steps")
    print("Final state:", world.get_state_info())
    
    if world.is_terminated():
        print("SUCCESS: All dirt cleaned!")
    else:
        print("FAILED: Simulation stopped witohut the problem being solved")


def run_with_gui(world: World, agent: IntelligentVacuumAgent, cell_size: int):
    print("Starting GUI...")
    
    viewer = PygameViewer(world, agent, cell_size=cell_size)
    world.add_observer(viewer)
    
    print("[bold]Controls:")
    print("[white]  SPACE - Pause/Resume")
    print("[white]  E - Toggle expanded nodes display")
    print("[white]  P - Toggle path display")
    print("[white]  +/- - Adjust simulation speed")
    print("[white]  ESC - Exit")
    print()
    print("The agent will start moving automatically using the selected search algorithm.")
    
    try:
        viewer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
    