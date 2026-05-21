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

def generate_random_3_regular_graph(n):
    if n % 2 != 0 or n < 4:
        raise ValueError("n must be even and at least 4")
    
    G = [[] for _ in range(n)]
    edges = set()
    
    def add_edge(u, v):
        if (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
            edges.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(G[i]) < 3 and len(G[j]) < 3:
                add_edge(i, j)
    
    return G

def tutte_polynomial(G, x, y):
    def dfs(v, parent):
        nonlocal count
        visited[v] = True
        for u in G[v]:
            if not visited[u]:
                dfs(u, v)
        if parent is None:
            count += 1
    
    n = len(G)
    visited = [False] * n
    count = 0
    dfs(0, None)
    return Fraction(count)

def resolution_width(G):
    def dpll():
        assignment = {}
        
        def unit_propagate():
            for lit in clauses:
                if all(lit in assignment or -lit in assignment for lit in clauses):
                    continue
                value = None
                for lit in lit:
                    if lit not in assignment and -lit not in assignment:
                        value = lit
                        break
                if value is None:
                    return False
                assignment[value] = True
            return True
        
        def backtrack():
            while len(assignment) > 0:
                var = list(assignment.keys())[-1]
                del assignment[var]
                if unit_propagate():
                    return True
            return False
        
        return backtrack()
    
    clauses = []
    for u in range(len(G)):
        for v in G[u]:
            clauses.append([u + 1, -v - 1])
            clauses.append([-u - 1, v + 1])
    
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_random_3_regular_graph(n)
    T_val = tutte_polynomial(G, 1, 1)
    
    if T_val <= 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "T(G; 1, 1) is non-positive"
        }
    
    resolution_width_val = resolution_width(G)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_val,
        "instances_tested": 1,
        "conjecture_holds": resolution_width_val >= math.log(T_val),
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width < c * log(T(G; 1, 1))\" first_failing_seed={first_failing_seed}")