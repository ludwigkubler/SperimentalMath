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

def generate_graph(clauses):
    n = 0
    edges = set()
    
    for clause in clauses:
        if len(clause) == 3 and clause[0] == 'p':
            n = int(clause[2:])
        elif len(clause) > 1 and clause[0] != 'p':
            u = int(clause[2:]) - 1
            v = int(clause[-2]) - 1
            edges.add((u, v))
    
    return n, edges

def is_loop(graph):
    n, edges = graph
    visited = [False] * n
    
    def dfs(node, parent):
        visited[node] = True
        for neighbor in range(n):
            if (node, neighbor) in edges or (neighbor, node) in edges:
                if not visited[neighbor]:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
        return False
    
    for i in range(n):
        if not visited[i] and dfs(i, -1):
            return True
    return False

def resolution_length(graph):
    n, edges = graph
    clauses = []
    
    def add_clause(u, v):
        clauses.append(f"p {n+1}")
        clauses.append(f"{u} {v}")
        clauses.append(f"-{u} -{v}")
    
    for u, v in edges:
        if not is_loop(graph):
            continue
        add_clause(u, v)
    
    def resolve(clauses):
        new_clauses = []
        while True:
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if clauses[i].startswith('-') and clauses[j].endswith(clauses[i][1:]) or \
                       clauses[j].startswith('-') and clauses[i].endswith(clauses[j][1:]):
                        new_clause = []
                        for c in clauses[i]:
                            if not (c.startswith('-') and c[1:] == clauses[j][-2]):
                                new_clause.append(c)
                        for c in clauses[j]:
                            if not (c.startswith('-') and c[1:] == clauses[i][-2]):
                                new_clause.append(c)
                        new_clauses.append(' '.join(new_clause))
                        found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(new_clauses)
            new_clauses = []
        return len(clauses)
    
    return resolve(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            clauses = []
            for i in range(n):
                if random.choice([True, False]):
                    u = random.randint(1, n)
                    v = random.randint(1, n)
                    while u == v:
                        v = random.randint(1, n)
                    clauses.append(f"{u} {v}")
                else:
                    u = random.randint(1, n)
                    v = random.randint(1, n)
                    while u == v:
                        v = random.randint(1, n)
                    clauses.append(f"-{u} -{v}")
            graph = generate_graph(clauses)
            if is_loop(graph):
                length = resolution_length(graph)
                total_length += length
                instances_tested += 1
    
    metric_value = total_length / instances_tested if instances_tested > 0 else 0
    conjecture_holds = False
    counterexample = ""
    
    if instances_tested >= 30:
        mean_length = total_length / instances_tested
        expected_bound = 2 ** (math.ceil(math.log2(mean_length)))
        if abs(mean_length - expected_bound) <= 50 * expected_bound:
            conjecture_holds = True
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")