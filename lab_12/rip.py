class Node:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.INF = 'inf'
        self.routing_table = {node: (1, node) for node in self.neighbors}

    def get_distance(self, key):
        if key in self.routing_table:
            return self.routing_table[key][0]
        return self.INF

    def update_routing_table(self, key, new_value, next_hop):
        if new_value != self.INF and (key not in self.routing_table or new_value + 1 < self.routing_table[key][0]):
            self.routing_table[key] = (new_value + 1, next_hop)
            return True
        return False

    def print_routing_table(self):
        print(f'{"[Source IP]":25} {"[Destination IP]":25} {"[Next Hop]":25} {"Metric":25}')
        for dest_router in self.routing_table:
            print(f'{self.name:25} {dest_router:25} {self.routing_table[dest_router][1]:25} '
                  f'{str(self.routing_table[dest_router][0]):25}')


class Network:
    def __init__(self, nodes):
        self.nodes = nodes

    def rip(self):
        step = 0
        is_changed = True
        while is_changed:
            step += 1
            is_changed = False
            for src in self.nodes:
                for dest in self.nodes:
                    if src.name == dest.name:
                        continue
                    for next_node in src.neighbors:
                        is_changed |= src.update_routing_table(dest.name, dest.get_distance(next_node), next_node)
                print(f'Simulation step {step} of router {src.name}:')
                src.print_routing_table()
                print()
            for node in self.nodes:
                print(f'Final state of router {node.name}:')
                node.print_routing_table()
                print()


def get_graph_structure(filepath: str):
    graph_dict = {}

    with open(filepath) as f:
        lines = f.readlines()

        for line in lines:
            v1, v2 = [int(s) for s in line.split()]

            if v1 in graph_dict.keys():
                graph_dict[v1].append(v2)
            else:
                graph_dict[v1] = [v2]

            if v2 in graph_dict.keys():
                graph_dict[v2].append(v1)
            else:
                graph_dict[v2] = [v1]

    return graph_dict


def get_nodes_ips(filepath: str):
    ips_dict = {}

    with open(filepath) as f:
        lines = f.readlines()

        for line in lines:
            node_id = int(line.split()[0])
            node_ip = str(line.split()[1])
            ips_dict[node_id] = node_ip

    return ips_dict


if __name__ == '__main__':
    INIT_GRAPH_INFO_FILE = 'config/init_network_graph.txt'
    IPS_INFO_FILE = 'config/ips.txt'

    graph = get_graph_structure(INIT_GRAPH_INFO_FILE)
    nodes_ips = get_nodes_ips(IPS_INFO_FILE)

    nodes = []

    for node_idx, node_ip in nodes_ips.items():
        neighbors_ids = graph[node_idx] if node_idx in graph else []
        neighbors_ips = [nodes_ips[num] for num in neighbors_ids]
        nodes.append(Node(node_ip, neighbors_ips))

    network = Network(nodes)
    network.rip()
