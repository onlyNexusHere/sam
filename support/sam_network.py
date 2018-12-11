import networkx as nx


class SamNetwork:

    sam_map = None

    def __init__(self):
        self.sam_map = nx.DiGraph()
        self.sam_map.add_node(1, location=(0, 0, 0))
        self.sam_map.add_node(2, location=(0, 0, 0))
        self.sam_map.add_node(3, location=(0, 0, 0))
        self.sam_map.add_node(4, location=(0, 0, 0))
        self.sam_map.add_node(5, location=(0, 0, 0))
        self.sam_map.add_node(6, location=(0, 0, 0))
        self.sam_map.add_node(7, location=(0, 0, 0))
        self.sam_map.add_node(8, location=(0, 0, 0))
        self.sam_map.add_node(9, location=(0, 0, 0))
        self.sam_map.add_node(10, location=(0, 0, 0))
        self.sam_map.add_node(11, location=(0, 0, 0))
        self.sam_map.add_node(12, location=(0, 0, 0))

        self.sam_map.add_node(100, location=(0, 0, 0))
        self.sam_map.add_node(200, location=(0, 0, 0))
        self.sam_map.add_node(300, location=(0, 0, 0))
        self.sam_map.add_node(400, location=(0, 0, 0))
        self.sam_map.add_node(500, location=(0, 0, 0))
        self.sam_map.add_node(600, location=(0, 0, 0))
        self.sam_map.add_node(700, location=(0, 0, 0))
        self.sam_map.add_node(800, location=(0, 0, 0))
        self.sam_map.add_node(900, location=(0, 0, 0))
        self.sam_map.add_node(1000, location=(0, 0, 0))
        self.sam_map.add_node(1100, location=(0, 0, 0))
        self.sam_map.add_node(1200, location=(0, 0, 0))

        self.sam_map.add_edge(1, 1200, func=self.straight_turn, max_sd=10)
        self.sam_map.add_edge(1, 400, func=self.left_turn, max_sd=10)

        self.sam_map.add_edge(2, 400, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(2, 800, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(3, 800, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(3, 1200, func=self.left_turn, max_sd=10)

        self.sam_map.add_edge(4, 1100, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(4, 700, func=self.left_turn, max_sd=10)

        self.sam_map.add_edge(5, 300, func=self.left_turn, max_sd=10)
        self.sam_map.add_edge(5, 700, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(6, 300, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(6, 1100, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(7, 100, func=self.left_turn, max_sd=10)
        self.sam_map.add_edge(7, 1000, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(8, 600, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(8, 1000, func=self.left_turn, max_sd=10)

        self.sam_map.add_edge(9, 100, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(9, 600, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(10, 500, func=self.left_turn, max_sd=10)
        self.sam_map.add_edge(10, 200, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(11, 200, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(11, 900, func=self.straight_turn, max_sd=10)

        self.sam_map.add_edge(12, 900, func=self.right_turn, max_sd=10)
        self.sam_map.add_edge(12, 500, func=self.left_turn, max_sd=10)

        self.sam_map.add_edge(100, 1, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(200, 2, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(300, 3, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(400, 4, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(500, 5, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(600, 6, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(700, 7, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(800, 8, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(900, 9, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(1000, 10, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(1100, 11, func=self.lane_follow, max_sd=20)
        self.sam_map.add_edge(1200, 12, func=self.lane_follow, max_sd=20)

    # States as functions:
    def lane_follow(self):
        pass

    def right_turn(self):
        pass

    def left_turn(self):
        pass

    def straight_turn(self):
        pass
