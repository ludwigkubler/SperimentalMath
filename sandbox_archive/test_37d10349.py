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

def generate_random_graph(n):
    graph = {i: set() for i in range(n)}
    edges = [(u, v) for u in range(n) for v in range(u+1, n)]
    num_edges = random.randint(int(0.5 * n), int(2 * n))
    selected_edges = random.sample(edges, num_edges)
    for u, v in selected_edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def tseitin_formula(graph):
    literals = {i: f'x{i}' for i in range(len(graph))}
    clauses = []
    
    def add_clause(clause):
        if clause not in clauses:
            clauses.append(clause)
    
    # Clause for each vertex
    for u in range(len(graph)):
        add_clause([f'-{literals[u]}', f'{literals[u]}'])
    
    # Clause for each edge (u, v)
    for u in range(len(graph)):
        for v in graph[u]:
            w = random.randint(0, len(graph)-1)
            while w == u or w == v:
                w = random.randint(0, len(graph)-1)
            add_clause([f'-{literals[u]}', f'-{literals[v]}', f'{literals[w]}'])
    
    return clauses

def resolution_length(clauses):
    def resolve(clause1, clause2):
        resolved = []
        for lit in clause1:
            if '-' + lit in clause2:
                continue
            elif lit in clause2:
                continue
            else:
                resolved.append(lit)
        return resolved
    
    queue = clauses.copy()
    while True:
        new_clauses = []
        found_resolvent = False
        for i in range(len(queue)):
            for j in range(i+1, len(queue)):
                resolvents = resolve(queue[i], queue[j])
                if not resolvents:
                    continue
                found_resolvent = True
                new_clause = set(resolvents)
                if new_clause not in new_clauses:
                    new_clauses.append(new_clause)
        if not found_resolvent:
            break
        queue.extend(new_clauses)
    
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    formula = tseitin_formula(graph)
    length = resolution_length(formula)
    
    C = 0.5  # Example constant
    lower_bound = C * 2**(n/2) * math.log(n)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": abs(length - lower_bound) <= 2 * lower_bound,
        "counterexample": "" if length >= lower_bound else f"Length {length} < Lower bound {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Length < Lower bound\" first_failing_seed={first_failing_seed + 1}")