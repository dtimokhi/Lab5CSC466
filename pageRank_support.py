import numpy as np
from collections import defaultdict
import time

class Graph:
    '''
        Graph class for creating the graphs for each dataset
    '''
    def __init__(self, directed = False):
        self._edge_dict = defaultdict(list)
        self._node_out_degree = defaultdict(int)
        self._directed = directed
        self._unique_edges = defaultdict(int)
    def __iter__(self):
        return iter(self._edge_dict.items())
    def __getitem__(self, key):
        return self._edge_dict[key]
    def add_edge(self, vert_1, vert_2, weight = 0):
        '''
        :param vert_1: node one
        :param vert_2: node two
        :param weight: weight of nodes
        :return:
        '''
        self._node_out_degree[vert_2] += 1
        self._edge_dict[vert_1].append((vert_2, weight))
        if not self._directed:
            self._node_out_degree[vert_1] += 1
            self._edge_dict[vert_2].append((vert_1, weight))
        self._unique_edges[vert_1] = 0;
        self._unique_edges[vert_2] = 0;
    def pop(self, node):
        self._edge_dict.pop(node, None)
    def count(self):
        '''
        :return: number of elements in graph
        '''
        return len(self._edge_dict)
    def get_dict(self):
        '''
        :return: the dictionary graph
        '''
        return self._edge_dict
    def keys(self):
        '''
        :return: returns the keys of the dictionary
        '''
        return self._edge_dict.keys()
    def set_direction(self, direction):
        '''
        :param direction: direction to set too
        :return: none
        '''
        self._directed = direction
    def add_key(self, key):
        self._edge_dict[key] = []
    def get_out_d(self, key):
        return self._node_out_degree[key]
    def get_unique_nodes(self):
        '''
        :return: returns all unique nodes
        '''
        return self._unique_edges


def make_graph(file_name, directed = False):
    '''
    :param file_name: file to make dataset for
    :param directed: directed or undirected graph
    :return: graph, end time
    '''
    start_time = time.time()
    graph = Graph(directed)
    with open(file_name) as file_object:
        for line in file_object:
            line_list = [x.strip() for x in line.replace("\n", "").replace('"', '').split(",")]
            start_edge = line_list[2]; end_edge = line_list[0]
            if "NCAA" in file_name and int(line_list[3].strip()) > int(line_list[1].strip()):
                start_edge = line_list[0]; end_edge = line_list[2]
                graph.set_direction(True)
            graph.add_edge(start_edge, end_edge, line_list[1])
    end = round(time.time() - start_time, 5)
    return graph, end

def make_graph_snap(file_name):
    '''
    :param file_name: makes a graph for snap datasets
    :return: graph
    '''
    start_time = time.time()
    graph = Graph(directed = True)
    with open(file_name) as file_parse:
        for line in file_parse:
            if "#" not in line:
                line_list = line.replace("\n", "").split("\t")
                graph.add_edge(int(line_list[1]), int(line_list[0]))
    end = round(time.time() - start_time, 5)
    return graph, end


def page_rank(graph, d, e):
    '''
    :param graph: graph of the dataset at hand
    :param d: probability
    :param e: distance cutoff
    :return: rankings, iterations, time
    '''
    start_time = time.time()
    prob = 1.0 / graph.count()
    unique = graph.get_unique_nodes().keys()
    # First Iteration
    pg = [];
    pg.append({k: prob for k, v in graph.get_unique_nodes().items()})

    # Second Iteration
    pg.append({node: (1 - d) * prob + d * sum(
        (1 / graph.get_out_d(in_node[0])) * (pg[0][in_node[0]]) for in_node in graph[node]) for node in unique})
    # Rest of the iteration
    r = 1
    while np.abs(sum(pg[r][key] - pg[r - 1][key] for key in pg[r])) > e:
        pg.append({node: (1 - d) * prob + d * sum(
            (1 / graph.get_out_d(in_node[0])) * (pg[r][in_node[0]]) for in_node in graph[node]) for node in
                   unique})
        r += 1
    end = round(time.time() - start_time, 5)
    return pg[r], r + 1, end


def run_page_rank(filename, d, e, snap=False):
    '''
    :param filename: file data
    :param d: probabiltiy
    :param e: distance cutoff
    :param snap: snap data or not
    :return: none
    '''
    if not snap:
        graph, graph_time = make_graph(filename)
    else:
        graph, graph_time = make_graph_snap(filename)
    rank, r, page_time = page_rank(graph, d, e)
    print("Time to produce graph: %.5f" % graph_time)
    print("Time to produce page-ranks: %.5f" % page_time)
    print("Number of iterations: %d" % r)

    rank_sorted = sorted(rank.items(), key=lambda x: x[1], reverse=True)
    with open("ranks.txt", "w") as file:
        for key, value in rank_sorted:
            file.write(str(key) + "," + str(round(value, 5)) + "\n")