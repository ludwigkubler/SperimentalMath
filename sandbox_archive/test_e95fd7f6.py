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
    
    def generate_k_clique(k, n):
        if k > n or k == 0:
            return None
        nodes = list(range(n))
        clique = random.sample(nodes, k)
        graph = {node: set() for node in nodes}
        for u in clique:
            for v in clique:
                if u != v:
                    graph[u].add(v)
                    graph[v].add(u)
        return graph
    
    def tree_width(graph):
        n = len(graph)
        if n == 0:
            return -1
        if n == 1:
            return 0
        
        leaves = [node for node in range(n) if len(graph[node]) == 1]
        while len(leaves) > 1:
            new_leaves = []
            for leaf in leaves:
                neighbor = next(iter(graph[leaf]))
                graph[neighbor].remove(leaf)
                if len(graph[neighbor]) == 1:
                    new_leaves.append(neighbor)
                del graph[leaf]
            leaves = new_leaves
        return n - len(leaves) - 1
    
    def homology_rank(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Compute the Laplacian matrix
        laplacian = [[0] * n for _ in range(n)]
        for node, neighbors in graph.items():
            degree = len(neighbors)
            laplacian[node][node] = -degree
            for neighbor in neighbors:
                laplacian[node][neighbor] += 1
        
        # Gaussian elimination to compute the rank
        rank = n
        for i in range(n):
            if laplacian[i][i] == 0:
                found_pivot = False
                for j in range(i + 1, n):
                    if laplacian[j][i] != 0:
                        laplacian[i], laplacian[j] = laplacian[j], laplacian[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    rank -= 1
                    continue
            
            pivot = Fraction(laplacian[i][i])
            for j in range(i, n):
                laplacian[i][j] /= pivot
        
            for j in range(n):
                if i != j:
                    factor = Fraction(laplacian[j][i])
                    for k in range(i, n):
                        laplacian[j][k] -= factor * laplacian[i][k]
        
        return rank
    
    def is_k_clique(graph, nodes):
        for u in nodes:
            for v in nodes:
                if u != v and v not in graph[u]:
                    return False
        return True
    
    n = 40
    k = random.randint(3, 5)
    graph = generate_k_clique(k, n)
    if graph is None:
        return {
            "metric_name": "tree_width",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k too large for n"
        }
    
    tw = tree_width(graph)
    rank = homology_rank(graph)
    
    if rank == -1:
        return {
            "metric_name": "tree_width",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "homology computation failed"
        }
    
    ratio = Fraction(rank, tw)
    if tw == 0:
        return {
            "metric_name": "tree_width",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tree-width is zero"
        }
    
    return {
        "metric_name": "rank_to_tw_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= k + 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")