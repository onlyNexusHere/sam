
import sys
import networkx as nx


sammap = nx.DiGraph()
sammap.add_node(1, location=(0, 0, 0))
sammap.add_node(2, location=(0, 0, 0))
sammap.add_node(3, location=(0, 0, 0))
sammap.add_node(4, location=(0, 0, 0))
sammap.add_node(5, location=(0, 0, 0))
sammap.add_node(6, location=(0, 0, 0))
sammap.add_node(7, location=(0, 0, 0))
sammap.add_node(8, location=(0, 0, 0))
sammap.add_node(9, location=(0, 0, 0))
sammap.add_node(10, location=(0, 0, 0))
sammap.add_node(11, location=(0, 0, 0))
sammap.add_node(12, location=(0, 0, 0))
# self made nodes to add simplicity.
sammap.add_node(100, location=(0, 0, 0))
sammap.add_node(200, location=(0, 0, 0))
sammap.add_node(300, location=(0, 0, 0))
sammap.add_node(400, location=(0, 0, 0))
sammap.add_node(500, location=(0, 0, 0))
sammap.add_node(600, location=(0, 0, 0))
sammap.add_node(700, location=(0, 0, 0))
sammap.add_node(800, location=(0, 0, 0))
sammap.add_node(900, location=(0, 0, 0))
sammap.add_node(1000, location=(0, 0, 0))
sammap.add_node(1100, location=(0, 0, 0))
sammap.add_node(1200, location=(0, 0, 0))

sammap.add_edge(1, 1200, func='straight_turn', max_sd=10)
sammap.add_edge(1, 400, func='left_turn', max_sd=10)

sammap.add_edge(2, 400, func='right_turn', max_sd=10)
sammap.add_edge(2, 800, func='straight_turn', max_sd=10)

sammap.add_edge(3, 800, func='right_turn', max_sd=10)
sammap.add_edge(3, 1200, func='left_turn', max_sd=10)

sammap.add_edge(4, 1100, func='right_turn', max_sd=10)
sammap.add_edge(4, 700, func='left_turn', max_sd=10)

sammap.add_edge(5, 300, func='left_turn', max_sd=10)
sammap.add_edge(5, 700, func='straight_turn', max_sd=10)

sammap.add_edge(6, 300, func='right_turn', max_sd=10)
sammap.add_edge(6, 1100, func='straight_turn', max_sd=10)

sammap.add_edge(7, 100, func='left_turn', max_sd=10)
sammap.add_edge(7, 1000, func='straight_turn', max_sd=10)

sammap.add_edge(8, 600, func='right_turn', max_sd=10)
sammap.add_edge(8, 1000, func='left_turn', max_sd=10)

sammap.add_edge(9, 100, func='right_turn', max_sd=10)
sammap.add_edge(9, 600, func='straight_turn', max_sd=10)

sammap.add_edge(10, 500, func='straight_turn', max_sd=10)
sammap.add_edge(10, 200, func='left_turn', max_sd=10)

sammap.add_edge(11, 200, func='right_turn', max_sd=10)
sammap.add_edge(11, 900, func='straight_turn', max_sd=10)

sammap.add_edge(12, 900, func='right_turn', max_sd=10)
sammap.add_edge(12, 500, func='left_turn', max_sd=10)

# adding the edge from the self made nodes to the real nodes.
sammap.add_edge(100, 1, func='lane_follow', max_sd=10)
sammap.add_edge(200, 2, func='lane_follow', max_sd=10)
sammap.add_edge(300, 3, func='lane_follow', max_sd=10)
sammap.add_edge(400, 4, func='lane_follow', max_sd=10)
sammap.add_edge(500, 5, func='lane_follow', max_sd=10)
sammap.add_edge(600, 6, func='lane_follow', max_sd=10)
sammap.add_edge(700, 7, func='lane_follow', max_sd=10)
sammap.add_edge(800, 8, func='lane_follow', max_sd=10)
sammap.add_edge(900, 9, func='lane_follow', max_sd=10)
sammap.add_edge(1000, 10, func='lane_follow', max_sd=10)
sammap.add_edge(1100, 11, func='lane_follow', max_sd=10)
sammap.add_edge(1200, 12, func='lane_follow', max_sd=10)


if __name__ == '__main__':
    start = sys.argv[1]
    rest = sys.argv[2:]
    start = int(start)
    rest = [int(node) for node in rest]
    path = [start]
    for goal in rest:
        next_path = nx.shortest_path(sammap, path[-1], goal)
        path.extend(nx.shortest_path(sammap, path[-1], goal)[1:])
    print(path)
    print([node for node in path if node < 99])
        


