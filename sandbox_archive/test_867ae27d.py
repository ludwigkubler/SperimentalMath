# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import product, combinations

def generate_monomial(n):
    return tuple(random.choice([0, 1]) for _ in range(n))

def generate_threshold_function(n, k):
    minterms = list(product([0, 1], repeat=n))
    selected_minterms = random.sample(minterms, k)
    return lambda x: any(x[i] == m[i] for i, m in enumerate(selected_minterms))

def generate_monotone_2cnf(n):
    variables = set(range(n))
    clauses = []
    for _ in range(10):  # Generate a few random clauses
        clause = random.sample(variables, 2)
        clauses.append((clause[0], clause[1]))
    return lambda x: all(x[v] or not x[u] for u, v in clauses)

def generate_recursive_majority(n):
    if n == 3:
        return lambda x: (x[0] and x[1]) or (not x[0] and not x[2])
    else:
        subformula = generate_recursive_majority(n - 1)
        return lambda x: subformula(x[:n-1]) and (x[n-1] == 1)

def build_bipartite_graph(f):
    n = len(next(iter(f.keys())))
    minterms = list(product([0, 1], repeat=n))
    maxterms = [tuple(1 - m[i] for i in range(n)) for m in minterms]
    
    graph = {}
    for m in minterms:
        if m not in graph:
            graph[m] = set()
        for mt in maxterms:
            if mt not in graph:
                graph[mt] = set()
            if sum(m[i] != mt[i] for i in range(n)) == 1 and f(mt) == 1:
                graph[m].add(mt)
                graph[mt].add(m)
    
    return graph

def bfs_diameter(graph, start):
    queue = [start]
    visited = {start}
    distance = {start: 0}
    max_distance = 0
    
    while queue:
        current = queue.pop(0)
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[current] + 1
                max_distance = max(max_distance, distance[neighbor])
                queue.append(neighbor)
    
    return max_distance

def monotone_kw_depth(f):
    n = len(next(iter(f.keys())))
    memo = {}
    
    def minimax(state, depth=0):
        if state in memo:
            return memo[state]
        
        if all(f[i] for i in range(n)):
            return depth
        
        min_val = float('inf')
        for i in range(n):
            new_state = list(state)
            new_state[i] = 1 - new_state[i]
            min_val = min(min_val, minimax(tuple(new_state), depth + 1))
        
        memo[state] = min_val
        return min_val
    
    return minimax((0,) * n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        if n == 3:
            f = generate_threshold_function(n, 2)
        elif n == 8:
            f = generate_monotone_2cnf(n)
        elif n == 11:
            f = generate_recursive_majority(3)
        else:
            return {
                "metric_name": "monotone-KW depth",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        B_f = build_bipartite_graph(f)
        D_TS = bfs_diameter(B_f, (0,) * n)
        D_m = monotone_kw_depth(f)
        
        results.append({
            "n": n,
            "D_TS": D_TS,
            "D_m": D_m
        })
    
    if not results:
        return {
            "metric_name": "monotone-KW depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    D_TS_values = [r["D_TS"] for r in results]
    D_m_values = [r["D_m"] for r in results]
    
    if all(D_m >= math.log2(D_TS + 1) - 1 for D_m, D_TS in zip(D_m_values, D_TS_values)):
        slope, intercept = linear_regression(D_TS_values, D_m_values)
        if slope >= 0.9 and intercept >= -1.5:
            return {
                "metric_name": "monotone-KW depth",
                "metric_value": None,
                "instances_tested": len(results),
                "conjecture_holds": True,
                "counterexample": ""
            }
    
    for r in results:
        if r["D_m"] < math.log2(r["D_TS"] + 1) - 1:
            return {
                "metric_name": "monotone-KW depth",
                "metric_value": None,
                "instances_tested": len(results),
                "conjecture_holds": False,
                "counterexample": f"Depth {r['D_m']} < log2({r['D_TS']}+1) - 1 for n={r['n']}"
            }
    
    return {
        "metric_name": "monotone-KW depth",
        "metric_value": None,
        "instances_tested": len(results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))