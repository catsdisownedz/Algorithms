from rich.console import Console
from rich.live import Live
from rich.table import Table
from queue import PriorityQueue
import random
import time

class A_star:
    def __init__(self, console):
        self.console = console
        self.parrot_name = ""
        self.cols = 0
        self.rows = 0
        
    def generate_grid(self):
        self.console.print("[grey58]Our dear parrot accidentally lost his pirate dad's money,\nhelp him find the shortest way through the maze so that he doesn't stop giving him lebb![/grey58]")
        self.console.print("\nEnter the number of rows in the maze:")
        self.rows = int(input())
        self.console.print("Enter the number of columns in the maze:")
        self.cols = int(input())
        self.console.print("[grey58]Plot twist, you're the parrots father, how mean![/grey58]")
        self.console.print("Enter your parrot's name:")
        parrot_name = input()
        grid = [["[grey58].[/grey58]" for _ in range(self.cols)] for _ in range(self.rows)]
        
        parrot_pos = (0, random.randint(0, self.cols - 1))
        grid[parrot_pos[0]][parrot_pos[1]] = "🦜"
        
        money_pos = (self.rows - 1, random.randint(0, self.cols - 1))
        grid[money_pos[0]][money_pos[1]] = "💰"
        
        # making sure there is always a path between the parrot and money we7na bn3ml el x's by 70%
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in (parrot_pos, money_pos) and random.random() > 0.75:
                    grid[i][j] = "[red]x[/red]"
        
        return grid, parrot_pos, money_pos, parrot_name

    def display_grid(self, grid):
        table = Table(show_header=False, show_lines=False, style="grey19")
        for row in grid:
            table.add_row(*row)
        return table

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def time_distance(self):
        initial_time = 0.4
        starting_point = 10
        increase_interval = 10
        speed_increase = 0.15
        
        row_increments = max(0, (self.rows - starting_point) // increase_interval)
        col_increments = max(0, (self.cols - starting_point) // increase_interval)
        
        total_increments = row_increments + col_increments
        speed = initial_time * (1 - speed_increase * total_increments)
        
        min_speed = 0.0001
        speed = max(speed, min_speed)
        
        return speed
        

    def a_star_search(self, grid, start, goal):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        path = []
        live = Live(self.display_grid(grid), console=self.console, refresh_per_second=15)
        final_found = False
        speed = self.time_distance()
        self.console.print(f"[grey58]The speed of the search is {speed} seconds per step[/grey58]")
        with live:
            while not open_set.empty():
                _, current = open_set.get()
                if current == goal:
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.reverse()
                    final_found = True
                    return path,live, final_found

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) 
                        and grid[neighbor[0]][neighbor[1]] != "[red]x[/red]" and neighbor not in g_score):
                        tentative_g_score = g_score[current] + 1
                        if tentative_g_score < g_score.get(neighbor, float('inf')):
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score = tentative_g_score + self.heuristic(neighbor, goal)
                            open_set.put((f_score, neighbor))

                            # Mark path being explored with yellow 'o' for coins
                            if grid[neighbor[0]][neighbor[1]] == "[grey58].[/grey58]":
                                grid[neighbor[0]][neighbor[1]] = "[yellow]o[/yellow]"
                            live.update(self.display_grid(grid))
                            time.sleep(speed)

        return came_from, live, final_found

    def run_search(self):
        grid, start, goal, parrot_name = self.generate_grid()
        self.console.print(f"\n{parrot_name} (🦜) is looking for his master's money (💰)...\n")
        path, live, final_found = self.a_star_search(grid, start, goal)

        if final_found:
            with live:
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if grid[i][j] == "[yellow]o[/yellow]" and (i, j) not in path:
                            grid[i][j] = "[orange1]-[/orange1]"
                # Blink the final path
                for _ in range(8):  
                    for position in path:
                        if grid[position[0]][position[1]] != "💰" and grid[position[0]][position[1]] != "🦜":
                            grid[position[0]][position[1]] = "[grey58].[/grey58]"
                    live.update(self.display_grid(grid))
                    time.sleep(0.2)
                    
                    for position in path:
                        if grid[position[0]][position[1]] != "💰" and grid[position[0]][position[1]] != "🦜":
                            grid[position[0]][position[1]] = "[yellow]o[/yellow]"
                    live.update(self.display_grid(grid))
                    time.sleep(0.2)
            self.console.print(f"\n[green]You helped {parrot_name} find his master's money!\nGood work :)[/green]\n")
        else:
            for position in path:
                if grid[position[0]][position[1]] != "💰" and grid[position[0]][position[1]] != "🦜":
                    grid[position[0]][position[1]] = "[orange1]-[/orange1]"
            live.update(self.display_grid(grid))
            time.sleep(0.6)
            self.console.print("\n[red]Fail.[/]")
