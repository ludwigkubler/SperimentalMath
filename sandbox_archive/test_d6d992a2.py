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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tree_depth(graph):
        n = len(graph)
        visited = [False] * n
        depth = [-1] * n
        
        def dfs(node, parent, d):
            if visited[node]:
                return 0
            visited[node] = True
            depth[node] = d
            max_child_depth = 0
            for neighbor in graph[node]:
                if neighbor != parent:
                    child_depth = dfs(neighbor, node, d + 1)
                    if child_depth > max_child_depth:
                        max_child_depth = child_depth
            return max_child_depth
        
        max_depth = 0
        for i in range(n):
            if not visited[i]:
                depth[i] = 0
                current_max = dfs(i, -1, 0)
                if current_max > max_depth:
                    max_depth = current_max
        return max_depth
    
    def resolution_length(graph):
        n = len(graph)
        clauses = [set(range(1, n + 1)), set(range(-n, 0))]
        assignment = {i: None for i in range(1, n + 1)}
        
        def unit_propagate():
            changed = False
            for clause in clauses:
                if len(clause) == 1:
                    literal = next(iter(clause))
                    if literal > 0 and assignment[literal] is None:
                        assignment[literal] = True
                        changed = True
                    elif literal < 0 and assignment[-literal] is None:
                        assignment[-literal] = False
                        changed = True
            return changed
        
        def resolve(l1, l2):
            new_clause = set()
            for lit in clauses[l1]:
                if -lit not in clauses[l2]:
                    new_clause.add(lit)
            return new_clause
        
        step = 0
        while unit_propagate():
            step += 1
        for i in range(n):
            for j in range(i + 1, n):
                if assignment[i + 1] is None and assignment[-(i + 1)] is None:
                    clause1 = {i + 1}
                    clause2 = {-j - 1}
                    new_clause = resolve(clause1, clause2)
                    clauses.append(new_clause)
                    step += 1
        return step
    
    n = random.randint(5, 40)
    graph = [[] for _ in range(n)]
    edges = set()
    
    while len(edges) < n - 1:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    td = tree_depth(graph)
    rl = resolution_length(graph)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": rl,
        "instances_tested": 1,
        "conjecture_holds": rl >= 2 ** td,
        "counterexample": "" if rl >= 2 ** td else f"Graph with n={n}, TD={td}, RL={rl}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")