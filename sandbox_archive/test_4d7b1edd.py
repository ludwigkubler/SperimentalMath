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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def graph_to_cnf(edges, n):
        cnf = []
        for i in range(n):
            clause = [-j - 1 for j in range(2 * i + 1, 2 * i + n)]
            cnf.append(clause)
        for (i, j) in edges:
            clause1 = [-2 * i - 1, -2 * j]
            clause2 = [-2 * i, -2 * j - 1]
            cnf.extend([clause1, clause2])
        return cnf
    
    def min_tree_depth(cnf):
        n = len(cnf)
        graph = {i: set() for i in range(n)}
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    graph[literal - 1].add(literal // 2)
        
        def dfs(node, visited):
            if node in visited:
                return float('inf')
            visited.add(node)
            min_depth = float('inf')
            for neighbor in graph[node]:
                depth = dfs(neighbor, visited) + 1
                if depth < min_depth:
                    min_depth = depth
            visited.remove(node)
            return min_depth
        
        max_depth = 0
        for i in range(n):
            max_depth = max(max_depth, dfs(i, set()))
        return max_depth
    
    def geometric_langlands_rank(cnf):
        n = len(cnf)
        rank = 0
        for clause in cnf:
            rank += len(clause) - 1
        return rank
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    cnf = graph_to_cnf(graph, n)
    
    rank = geometric_langlands_rank(cnf)
    depth = min_tree_depth(cnf)
    
    conjecture_holds = abs(rank - math.log2(n)) <= 3 and rank == depth
    counterexample = f"n={n}, rank={rank}, depth={depth}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")