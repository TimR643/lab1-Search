#!/usr/bin/env python3
"""
Convenience script to run the vacuum world lab.
"""
import sys
import os

# Add the current directory to the path so we can import vacuum_world
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the main function
if __name__ == "__main__":
    from vacuum_world.main import main
    main()