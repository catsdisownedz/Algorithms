# Graph.py
from collections import defaultdict
import random
from rich.text import Text
from rich.live import Live

class Graph:
    def __init__(self, console):
        self.graph = defaultdict(list)
        self.root = None
        self.console = console
        self.node_colors = {}
        self.live = None
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def generate_random_tree(self, node_count):
        nodes = random.sample(range(1, 101), node_count)
        child_nodes = set()

        for i in range(1, node_count):
            parent = nodes[random.randint(0, i - 1)]
            child = nodes[i]
            self.add_edge(parent, child)
            child_nodes.add(child)
           # self.console.print(f"parent: {parent}, child: {child}")

        root_candidates = set(nodes) - child_nodes
        self.root = root_candidates.pop() if root_candidates else nodes[0]

    def build_text_tree(self, node=None, prefix="", is_last=True):
        if node is None:
            node = self.root
        branch = "└── " if is_last else "├── "
        color = self.node_colors.get(node, "white") 
        text = Text(prefix + branch + str(node), style=color)
        text.append("\n") 

        prefix += "    " if is_last else "│   "
        children = self.graph[node]
        for i, child in enumerate(children):
            is_last_child = i == (len(children) - 1)
            text.append(self.build_text_tree(child, prefix, is_last_child))
        
        return text

    def print_colored_tree(self):
        self.live = Live(self.build_text_tree(), console=self.console, refresh_per_second=20)
        self.live.start()
        return self.live

    def update_node_color(self, node, color):
        self.node_colors[node] = color
       # self.live.update(self.build_text_tree()) 