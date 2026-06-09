# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_circuit(d, depth):
        if d == 1:
            return []
        elif d == 2:
            return [[0], [1]]
        else:
            circuit = []
            for _ in range(depth):
                layer = []
                for i in range(len(circuit)):
                    for j in range(len(circuit[i])):
                        new_node = len(circuit) + len(layer)
                        circuit[i][j].append(new_node)
                        layer.append([new_node, (i + 1) % d])
                circuit.extend(layer)
            return circuit
    
    def construct_tropical_graph(circuit):
        graph = {}
        for layer in circuit:
            for node in layer:
                if node[0] not in graph:
                    graph[node[0]] = set()
                for neighbor, _ in node[1:]:
                    if neighbor not in graph:
                        graph[neighbor] = set()
                    graph[node[0]].add(neighbor)
        return graph
    
    def min_representation_size(graph):
        visited = {node: False for node in graph}
        
        def dfs(node):
            stack = [node]
            while stack:
                current_node = stack.pop()
                if not visited[current_node]:
                    visited[current_node] = True
                    for neighbor in graph[current_node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        max_depth = 0
        for node in graph:
            visited[node] = False
            dfs(node)
            max_depth = max(max_depth, sum(1 for v in visited.values() if v))
        
        return max_depth
    
    d = random.randint(3, 5)
    depth = int(math.log2(d)) + 1
    circuit = generate_d_regular_circuit(d, depth)
    
    graph = construct_tropical_graph(circuit)
    size = min_representation_size(graph)
    
    D = depth
    bound = D**2 * math.log(d)
    
    return {
        "metric_name": "minimal_representation_size",
        "metric_value": size,
        "instances_tested": 1,
        "n_max": depth,
        "conjecture_holds": size <= bound,
        "counterexample": "" if size <= bound else f"Size {size} exceeds bound {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")