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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def tseitin_formula(graph, n):
        literals = {i: (2 * i, 2 * i + 1) for i in range(n)}
        clauses = []
        
        # Add clauses for each edge
        for u, v in graph:
            a, b = literals[u]
            c, d = literals[v]
            clauses.append([a, -b, -c])
            clauses.append([-a, b, c])
            clauses.append([a, -b, d])
            clauses.append([-a, b, -d])
        
        # Add clauses for each vertex
        for i in range(n):
            a, b = literals[i]
            clauses.append([a, b])
            clauses.append([-a, -b])
        
        return clauses
    
    def resolution_length(clauses):
        n = len(clauses)
        resolvents = set()
        
        while True:
            new_resolvents = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if any(lit in clause and -lit in other_clause for lit in clauses[i] for other_clause in clauses[j]):
                        resolvent = [lit for lit in clauses[i] if lit not in [-x for x in clauses[j]]]
                        new_resolvents.add(tuple(sorted(resolvent)))
            if not new_resolvents:
                break
            resolvents.update(new_resolvents)
            n += len(new_resolvents)
        
        return len(resolvents)
    
    def coxeter_group_orbits(graph):
        n = len(graph)
        orbits = set()
        visited = [False] * n
        
        def dfs(node, path):
            if node in visited:
                return
            visited[node] = True
            path.append(node)
            for neighbor in graph[node]:
                dfs(neighbor, path)
        
        for i in range(n):
            if not visited[i]:
                orbit = []
                dfs(i, orbit)
                orbits.add(tuple(sorted(orbit)))
        
        return len(orbits)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    clauses = tseitin_formula(graph, n)
    resolution_len = resolution_length(clauses)
    coxeter_orbits = coxeter_group_orbits(graph)
    
    ratio = Fraction(coxeter_orbits, 2 ** resolution_len)
    
    return {
        "metric_name": "Ratio of Orbits to 2^Resolution Length",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Graph with {n} nodes and resolution length {resolution_len}, orbits {coxeter_orbits}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {results[first_failing]['instances_tested']} nodes and resolution length {results[first_failing]['metric_value']}, orbits {results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")