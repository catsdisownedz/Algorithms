import time

class DFS:
    def __init__(self, graph, target, console):
        self.graph = graph
        self.target = target
        self.console = console
        self.found = False

    def search(self, start, live):
        visited = set()
        self._dfs_recursive(start, visited, live)
        if not self.found:
            live.stop()
            self.console.print("\n[red]Target not found in the tree.[/]")

    def _dfs_recursive(self, node, visited, live):
        if node in visited or self.found:
            return
        visited.add(node)
        self.graph.update_node_color(node, "red")
        live.update(self.graph.build_text_tree(self.graph.root))
        time.sleep(0.5)

        if node == self.target:
            self.graph.update_node_color(node, "green")
            live.update(self.graph.build_text_tree(self.graph.root))
            time.sleep(1)
            live.stop()
            self.console.print(f"\n[green]Found target {self.target} in the tree![/]")
            self.found = True
            return

        for child in self.graph.graph[node]:
            self._dfs_recursive(child, visited, live)
            if self.found:
                return

        self.graph.update_node_color(node, "#555555")
        live.update(self.graph.build_text_tree(self.graph.root))
        time.sleep(0.5)
