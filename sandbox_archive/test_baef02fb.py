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

def hashimoto_operator(graph):
    V, E = graph
    n = len(V)
    m = len(E)
    B = [[0] * (2*m) for _ in range(2*m)]
    
    for (a, b), (c, d) in E:
        if b == c and a != d:
            B[2*a][2*m + 2*b] = 1
            B[2*c][2*m + 2*d] = 1
    
    return B

def spectral_gap(B):
    eigenvalues = [complex(eigenvalue) for eigenvalue in numpy.linalg.eigvals(B)]
    lambda_1 = max(abs(eigenvalue) for eigenvalue in eigenvalues)
    other_eigenvalues = [eigenvalue for eigenvalue in eigenvalues if abs(eigenvalue) != lambda_1 and eigenvalue != 0]
    if not other_eigenvalues:
        return 0
    lambda_max_other = max(abs(eigenvalue) for eigenvalue in other_eigenvalues)
    return math.log(lambda_1) - math.log(lambda_max_other)

def dpll_node_count(G, sigma):
    # Placeholder for DPLL node count estimation
    # This is a very rough approximation and should be replaced with actual logic
    n = len(G[0])
    m = len(G[1])
    return (n + m) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    graph_families = {
        "cycle": lambda n: ([i for i in range(n)] + [0], [(i, (i+1)%n) for i in range(n)]),
        "dumbbell": lambda n: ([i for i in range(n//2)] + [j+n//2 for j in range(n//2)], 
                               [(i, i+1) for i in range(n//2-1)] + [(j+n//2, j+n//2+1) for j in range(n//2-1)] + [(n//2-1, n//2)]),
        "random_3regular": lambda n: random_regular_graph(n, 3),
        "random_4regular": lambda n: random_regular_graph(n, 4),
        "path_of_triangles": lambda n: ([i for i in range(3*n)], [(i, i+1) for i in range(3*n-1)] + [(0, n), (n, 2*n)]),
        "complete_bipartite": lambda n: ([i for i in range(n//2)] + [j+n//2 for j in range(n//2)], 
                                        [(i, j+n//2) for i in range(n//2) for j in range(n//2)])
    }
    
    results = []
    for family_name, graph_func in graph_families.items():
        n_values = [8, 12, 16, 20, 28, 36]
        for n in n_values:
            G = graph_func(n)
            V, E = G
            sigma = {v: random.randint(0, 1) for v in V}
            
            B_G = hashimoto_operator(G)
            nu_G = spectral_gap(B_G)
            
            nodes = dpll_node_count(G, sigma)
            log_nodes = math.log2(nodes)
            
            results.append({
                "metric_name": "log2(DPLL_nodes)",
                "metric_value": log_nodes,
                "instances_tested": 1,
                "conjecture_holds": nu_G < 0.1 * math.log(n),
                "counterexample": ""
            })
    
    overall_conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if overall_conjecture_holds else "mapping_undefined"
    
    return {
        "seed": seed,
        "metric_name": "log2(DPLL_nodes)",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": overall_conjecture_holds,
        "counterexample": counterexample
    }

def random_regular_graph(n, k):
    if n * k % 2 != 0:
        raise ValueError("n*k must be even")
    
    V = list(range(n))
    E = []
    degrees = [k] * n
    
    for i in range(k):
        available_nodes = set(V) - {i}
        while degrees[i] > 0:
            j = random.choice(list(available_nodes))
            if (j, i) not in E and (i, j) not in E:
                E.append((i, j))
                degrees[i] -= 1
                degrees[j] -= 1
                available_nodes.remove(j)
    
    return V, E

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")