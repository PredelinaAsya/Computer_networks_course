import numpy as np
from typing import List


class Node:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.routing_table = {self.name: {self.name: 0}}
        self.is_updated = True

        for neighbor, cost in self.neighbors.items():
            self.routing_table[neighbor] = {self.name: cost}
            self.routing_table[self.name][neighbor] = cost
            for neighbor_2 in self.neighbors:
                self.routing_table[neighbor][neighbor_2] = np.inf
            self.routing_table[neighbor][neighbor] = 0

        print(f'        Node {self.name}: current distance vector = {self.routing_table[self.name]}')


    def send_routing_table(self):
        return self.routing_table[self.name]


    def update_routing_table(self, neighbor, routing_vector):
        self.routing_table[neighbor] = routing_vector
        for destination, distance in routing_vector.items():
            if destination not in self.routing_table[self.name]:
                self.routing_table[self.name][destination] = self.routing_table[self.name][neighbor] + distance
                self.is_updated = True
                print(f'        Node {self.name}: distance to {destination} added and equal to {self.routing_table[self.name][destination]}')
            elif self.routing_table[self.name][destination] > self.routing_table[self.name][neighbor] + distance:
                self.routing_table[self.name][destination] = self.routing_table[self.name][neighbor] + distance
                self.is_updated = True
                print(f'        Node {self.name}: distance to {destination} changed to {self.routing_table[self.name][destination]}')
        print(f'        Node {self.name}: current distance vector = {self.routing_table[self.name]}')

class Network:
    def __init__(self, nodes: List[Node]):
        self.nodes = {node.name: node for node in nodes}


    def update_network(self):
        while True:
            any_action_flag = False
            for node_name, node in self.nodes.items():
                if node.is_updated:
                    print(f'Network: node {node_name} expanded...')
                    for neighbor in node.neighbors:
                        print(f'    Network: sending package from {node_name} to {neighbor}')
                        self.nodes[neighbor].update_routing_table(node_name, node.send_routing_table())
                    node.is_updated = False
                    any_action_flag = True
            if not any_action_flag:
                break


    def change_edge_cost(self, node_1, node_2, new_cost):
        neigh_1 = self.nodes[node_1].neighbors
        neigh_1[node_2] = new_cost
        self.nodes[node_1] = Node(node_1, neigh_1)

        neigh_2 = self.nodes[node_2].neighbors
        neigh_2[node_1] = new_cost
        self.nodes[node_2] = Node(node_2, neigh_2)

        for node in self.nodes:
            if node != node_1 and node != node_2:
                self.nodes[node] = Node(node, self.nodes[node].neighbors)


def get_graph_structure(filepath: str):
    graph_dict = {}

    with open(filepath) as f:
        lines = f.readlines()
        n, m = [int(s) for s in lines[0].split()]

        for line in lines[1:]:
            v1, v2, c = [int(s) for s in line.split()]

            if v1 in graph_dict.keys():
                graph_dict[v1].append((v2, c))
            else:
                graph_dict[v1] = [(v2, c)]

            if v2 in graph_dict.keys():
                graph_dict[v2].append((v1, c))
            else:
                graph_dict[v2] = [(v1, c)]

    return graph_dict


def get_edge_costs_changes(filename: str):
    changed_edges_with_costs = []

    with open(filename) as f:
        lines = f.readlines()

        for line in lines:
            v1, v2, c = [int(s) for s in line.split()]
            changed_edges_with_costs.append((v1, v2, c))

    return changed_edges_with_costs


if __name__ == '__main__':
    INIT_GRAPH_INFO_FILE = './config/init_graph.txt'
    CHANGE_COSTS_IN_GRAPH = './config/change.txt'

    graph_dict = get_graph_structure(INIT_GRAPH_INFO_FILE)
    nodes = []

    for v in graph_dict:
        neighbors = {v2: c for v2, c in graph_dict[v]}
        nodes.append(Node(v, neighbors))

    network = Network(nodes)
    network.update_network()

    changed_edges_with_costs = get_edge_costs_changes(CHANGE_COSTS_IN_GRAPH)

    for v1, v2, c in changed_edges_with_costs:
        print(f'CHANGE EDGE COST BETWEEN {v1} AND {v2} TO {c}')
        network.change_edge_cost(v1, v2, c)

    network.update_network()
