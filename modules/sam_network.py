from .SamModule import SamModule
import networkx as nx
import random


class SamNetwork(SamModule):

    sam_map = None

    # Path planning current variables, these are nodes in the graph
    current_node = None
    next_node = None
    end_node = None

    # This is a set of end nodes, for if we get a set path to go on.
    path_to_follow = list()

    # Variable for if we want the robot to run randomly.
    # If the path_to_follow is empty, it will generate a random node to go to.
    generate_random_when_path_empty = False

    def __init__(self, kargs):
        super().__init__(module_name="Map", is_local=True, identi="map", **kargs)

                    # GRAPH
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
        # self-made nodes to add simplicity.
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

        # adding the edge from the self-made nodes to the real nodes.
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
    # They have the function calls for what exactly to do.
    # If pi control ping, need to send a request to motors and when to finish and when to timeout
    def lane_follow(self):
        # follow state until red line
        print("following lane")

    def right_turn(self):
        # follow state until location and headingq
        print("turning right")

    def left_turn(self):
        # follow state until location and heading
        print("turning left")

    def straight_turn(self):
        # follow sate until location and heading
        print("continuing straight")

    # Path functions for the robot:
    def set_current_node(self, node):
        n = self._get_node(node)
        if n is not None:
            self.current_node = n

    # Set a new goal node.
    # Saves end node back onto the path
    def set_end_node(self, node):
        n = self._get_node(node)
        if n is not None:
            if self.next_node is not None:
                self.path_to_follow = [int(self.end_node)] + self.path_to_follow
            self.end_node = n

    # Set a whole new path
    # This function resets the path, then adds to it
    def set_path(self, nodes_list):
        self.path_to_follow = list()

        if type(nodes_list) is int or type(nodes_list) is str:
            self.add_to_path(nodes_list)

        for node in nodes_list:
            self.add_to_path(node)

    # Add to the current set of nodes in the path
    def add_to_path(self, node):
        n = self._get_node(node)
        if n is not None:
            self.path_to_follow.append(n)

    def set_random_true(self):
        self.generate_random_when_path_empty = True

    def set_random_false(self):
        self.generate_random_when_path_empty = False

    def update_next_node(self):
        # bfs, as we don't have length attributes or accurate locations

        if self.current_node == self.end_node or self.end_node is None:

            if self.path_to_follow == list() and not self.generate_random_when_path_empty:
                print("Hit end of path!!")
                # TODO raise event
                return
            elif self.path_to_follow == list():
                self.path_to_follow = [random.randint(1, 12)]

            self.end_node = self.path_to_follow[0]
            self.path_to_follow = self.path_to_follow[1:]

        path = nx.shortest_path(self.sam_map, self.current_node, self.end_node)
        if len(path) < 2:
            print("Path of one or none, cannot make path from " + str(self.current_node) + " to " + str(self.end_node))
        self.next_node = path[1]

    def test_move_to_next(self):
        if self.current_node == self.next_node or self.next_node is None:
            self.update_next_node()

        if self.current_node is not self.next_node:
            if self.next_node in self.sam_map[self.current_node]:
                my_func = self.get_state_for_edge(self.current_node, self.next_node)
                if my_func is not None:
                    my_func()
                    print("Now at " + str(self.next_node))
                    self.current_node = int(self.next_node)
                else:
                    print("my_func was none")
            else:
                print("something went very wrong")

    def get_state_for_edge(self, node1=None, node2=None):
        if node1 is not None and node2 is not None:
            return self.sam_map.get_edge_data(node1, node2)['func']
        else:
            self.sam_map.get_edge_data(self.current_node, self.next_node)['func']

    # Supporting functions

    # Printing out current path information
    def show_current_vars_set(self):
        to_print = "\nCurrently at: " + str(self.current_node)
        to_print = to_print + "\nNext node is: " + str(self.next_node)
        to_print = to_print + "\nEnd node is: " + str(self.end_node)
        to_print = to_print + "\nUpcoming path is: " + str(self.path_to_follow)
        to_print = to_print + "\nRandom path generation: " + str(self.generate_random_when_path_empty)
        to_print = to_print + "\n"
        print(to_print)

    # Converting to an int if needed and making sure it is in the graph
    def _get_node(self, node):
        node_to_int = None
        try:
            node_to_int = int(node)
        except ValueError:
            print("Cannot assign non-integer")
            return

        if node_to_int in self.sam_map:
            return node_to_int
        else:
            return None

    def stdin_request(self, message):

        msg_parts = message.strip().split(" ")

        if len(msg_parts) < 2:
            return
        if msg_parts[0] == "random":
            if msg_parts[1] == 'true':
                self.set_random_true()
                return
            elif msg_parts[1] == 'false':
                self.set_random_false()
                return

        if len(msg_parts) < 3:
            return

        if msg_parts[0] == "set":
            if msg_parts[1] == 'current':
                self.set_current_node(msg_parts[2])
            elif msg_parts[1] == 'end':
                self.set_end_node(msg_parts[2])
            elif msg_parts[1] == 'path':
                self.set_end_node(msg_parts[2:])

    def message_received(self, message):
        if message.strip() == "ready":
            self.current_node = self.next_node

        # TODO add for following the path
