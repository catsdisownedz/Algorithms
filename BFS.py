from collections import deque
import time

class BFS:
    def __init__(self, graph, target, console):
        self.graph = graph
        self.target = target
        self.console = console

    def search(self, start, live):
        visited = set()
        queue = deque([start])

        while queue:
            node = queue.popleft()
            self.graph.update_node_color(node, "red")
            live.update(self.graph.build_text_tree(self.graph.root)) 
            time.sleep(0.6)

            if node == self.target:
                self.graph.update_node_color(node, "green")
                live.update(self.graph.build_text_tree(self.graph.root))
                time.sleep(1)
                live.stop()
                self.console.print(f"\n[green]Found target {self.target} in the tree![/]")
                return

            visited.add(node)
            for child in self.graph.graph.get(node, []):
                if child not in visited and child not in queue:
                    queue.append(child)

            self.graph.update_node_color(node, "#555555")  
            live.update(self.graph.build_text_tree(self.graph.root)) 
            time.sleep(0.5)

        live.stop()
        self.console.print("\n[red]Target not found in the tree.[/]")
