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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tropical_rank(cnf):
        vertices = set()
        edges = []
        for clause in cnf:
            for lit in clause:
                vertices.add(abs(lit))
                for other_lit in clause:
                    if lit != other_lit:
                        edges.append((abs(lit), abs(other_lit)))
        graph = {v: [] for v in vertices}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        max_depth = 0
        for v in vertices:
            visited = set()
            dfs(v, visited)
            max_depth = max(max_depth, len(visited))
        return max_depth
    
    def resolution_width(cnf):
        clauses = cnf[:]
        queue = []
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if abs(queue[i][0]) == abs(queue[j][1]):
                        resolvent = [x for x in queue[i] if x != queue[i][0]] + [x for x in queue[j] if x != -queue[j][1]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            queue.extend(new_clauses)
        return max(len(clause) for clause in queue)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mtr = tropical_rank(cnf)
    w = resolution_width(cnf)
    
    upper_bound = math.log2(n) + mtr
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": w <= upper_bound,
        "counterexample": "" if w <= upper_bound else f"w({n})={w}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        upper_bound = max(r["upper_bound"] for r in results)
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")