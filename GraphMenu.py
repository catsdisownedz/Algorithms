from rich.console import Console
from Graph import Graph
from BFS import BFS
from DFS import DFS
from A_star import A_star

class GraphMenu:
    
    def welcome():
        print("\033[95m\n\nWelcome to the Graph Algorithms Menu\033[0m")
        print("1. Uninformed Tree algorithms (BFS/DFS)")
        print("2. Informed Tree algorithms (A*)")
        print("\033[91m3. Exit\033[0m")
        
        choice = int(input("Enter your choice: "))
        return choice
    
    @staticmethod
    def run():
        console = Console()
        def get_valid_input(prompt, valid_type=int, condition=lambda x: True, error_message="Invalid input. Please try again."):
            while True:
                try:
                    user_input = valid_type(input(prompt))
                    if condition(user_input):
                        return user_input
                    else:
                        console.print(f"[red]{error_message}[/red]")
                except ValueError:
                    console.print(f"[red]{error_message}[/red]")
        while True:
            choice = GraphMenu.welcome()
            if choice == 1:
                graph = Graph(console)
                node_count = int(input("\033[95mEnter the number of nodes for the randomized graph: \033[0m"))
                graph.generate_random_tree(node_count)

                console.print("\nRandomly Generated Tree Structure:")
                graph.console.print(graph.build_text_tree(graph.root))

                target_number = get_valid_input("\nEnter the number you're looking for in the tree: ", int, lambda x: 0 <= x < node_count, "Invalid target number. Please enter a number between 0 and {node_count - 1}.")
                method = get_valid_input("Enter '1' for BFS or '2' for DFS: ", int, lambda x: x in [1, 2], "Invalid method. Please enter '1' for BFS or '2' for DFS.")

                console.print("\nTree Structure for Search:")

                if method == 1:
                    bfs = BFS(graph, target_number, console)
                    live = graph.print_colored_tree()
                    bfs.search(graph.root, live)
                elif method == 2:
                    dfs = DFS(graph, target_number, console)
                    live = graph.print_colored_tree()
                    dfs.search(graph.root, live)
            elif choice == 2:
                a_star = A_star(console)
                a_star.run_search()
            elif choice == 3:
                print("\033[95m\n\nThank you for using my eftekasat >:D \033[0m")
                break           
        
if __name__ == "__main__":
    GraphMenu.run()
