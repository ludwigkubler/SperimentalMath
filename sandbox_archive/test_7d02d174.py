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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def tree_depth(graph):
    n = len(graph)
    visited = [False] * n
    depth = 0
    
    def dfs(node, current_depth):
        nonlocal depth
        if current_depth > depth:
            depth = current_depth
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, current_depth + 1)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, 1)
    
    return depth

def resolution_length(clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)
    
    unit_clauses = {l: [] for l in literals}
    for clause in clauses:
        if len(clause) == 1:
            unit_clauses[clause[0]].append(clause)
    
    resolution_steps = 0
    while True:
        new_unit_clauses = {}
        found_new_clause = False
        
        for literal, unit_clauses_list in unit_clauses.items():
            for clause in unit_clauses_list:
                if -literal in literals:
                    new_literal = -literal
                    new_clause = [l for l in clause if l != literal]
                    new_clause.append(new_literal)
                    
                    if new_clause not in clauses:
                        clauses.add(tuple(sorted(new_clause)))
                        found_new_clause = True
                        new_unit_clauses[new_literal] = new_unit_clauses.get(new_literal, []) + [new_clause]
        
        if not found_new_clause:
            break
        
        unit_clauses = new_unit_clauses
        resolution_steps += 1
    
    return resolution_steps

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = [[] for _ in range(n)]
    for _ in range(random.randint(int(0.5 * n * (n - 1)), int(0.8 * n * (n - 1)))):
        u, v = random.sample(range(n), 2)
        if v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
    
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append((i, -j))
            clauses.append((-i, j))
    
    depth = tree_depth(graph)
    length = resolution_length(set(tuple(sorted(c)) for c in clauses))
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** depth,
        "counterexample": "" if length >= 2 ** depth else f"Graph with n={n}, A={graph}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")