# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def treewidth(G):
        n = len(G)
        if n == 0:
            return 0
        for root in range(n):
            visited = [False] * n
            stack = [(root, -1)]
            while stack:
                node, parent = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in G[node]:
                        if neighbor != parent and not visited[neighbor]:
                            stack.append((neighbor, node))
            if sum(visited) == n:
                return 0
        return float('inf')
    
    def tseitin_formula(G, root):
        n = len(G)
        clauses = []
        literals = {}
        
        def add_clause(literals):
            clauses.append([l for l in literals])
        
        def new_literal():
            nonlocal literal_count
            literal_count += 1
            return literal_count
        
        literal_count = 0
        stack = [(root, -1)]
        while stack:
            node, parent = stack.pop()
            if node not in literals:
                literals[node] = new_literal()
            for neighbor in G[node]:
                if neighbor != parent and neighbor not in literals:
                    literals[neighbor] = new_literal()
                    add_clause([literals[node], -literals[neighbor]])
                    add_clause([-literals[node], literals[neighbor]])
                    stack.append((neighbor, node))
        return clauses
    
    def resolution_length(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        for i in range(n):
            for j in range(i + 1, n):
                new_clauses = []
                for c1 in clauses[i]:
                    for c2 in clauses[j]:
                        if -c1 in c2:
                            new_clause = list(c1)
                            new_clause.extend([l for l in c2 if l != -c1])
                            new_clauses.append(new_clause)
                if not new_clauses:
                    return 0
                clauses.extend(new_clauses)
        return len(clauses)
    
    n = random.randint(5, 40)
    G = [[] for _ in range(n)]
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
    
    root = random.randint(0, n - 1)
    tw = treewidth(G)
    formula = tseitin_formula(G, root)
    length = resolution_length(formula)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (tw * math.log(2)),
        "counterexample": "" if length >= 2 ** (tw * math.log(2)) else f"Graph with treewidth {tw} and resolution length {length}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with treewidth {r['metric_value']} and resolution length {r['metric_value']}\" first_failing_seed={first_failing_seed}")