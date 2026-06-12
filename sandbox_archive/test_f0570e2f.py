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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) == d and len(graph[j]) == d:
                    continue
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def mls(graph):
        n = len(graph)
        if n == 0:
            return 0
        rank = 1
        for i in range(n):
            neighbors = set(graph[i])
            subgraph_rank = 0
            for j in range(n):
                if j != i and j not in neighbors:
                    subgraph = [k for k in range(n) if k != j and k not in neighbors]
                    subgraph_rank += mls(subgraph)
            rank = max(rank, subgraph_rank + 1)
        return rank
    
    def psat(graph):
        n = len(graph)
        literals = list(range(2 * n))
        assignment = [None] * (2 * n)
        
        def dfs(node, level):
            if level == n:
                return True
            for neighbor in graph[node]:
                if assignment[neighbor] is not None and assignment[neighbor] == assignment[node]:
                    continue
                assignment[neighbor] = 1 - assignment[node]
                if dfs(neighbor, level + 1):
                    return True
                assignment[neighbor] = None
            return False
        
        for i in range(n):
            assignment[i] = 0
            if not dfs(i, 0):
                return float('inf')
        
        def count_clauses():
            clauses = []
            for node in range(n):
                clause = [literals[node], literals[2 * n - node - 1]]
                clauses.append(clause)
                for neighbor in graph[node]:
                    clause = [-literals[neighbor], literals[node]]
                    clauses.append(clause)
                    clause = [-literals[node], literals[2 * n - neighbor - 1]]
                    clauses.append(clause)
            return len(clauses)
        
        return count_clauses()
    
    d_values = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    for d in d_values:
        n_max = 20
        instances_tested = 0
        mls_sum = 0
        psat_sum = 0
        
        while instances_tested < 30:
            graph = generate_d_regular_graph(n_max, d)
            if graph is None:
                continue
            mls_value = mls(graph)
            psat_value = psat(graph)
            
            if mls_value == 0 or psat_value == float('inf'):
                continue
            
            results.append((mls_value, psat_value))
            instances_tested += 1
    
    if not results:
        return {
            "metric_name": "mls(G) / PSAT(φ_G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mls_values, psat_values = zip(*results)
    mls_mean = sum(mls_values) / len(mls_values)
    psat_mean = sum(psat_values) / len(psat_values)
    support_fraction = sum(1 for mls, psat in results if mls >= 0.75 * psat) / len(results)
    
    return {
        "metric_name": "mls(G) / PSAT(φ_G)",
        "metric_value": mls_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={sum(1 for r in results if 'conjecture_holds' in r and r['conjecture_holds']) / len(results)}")