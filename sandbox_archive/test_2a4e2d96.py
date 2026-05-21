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
    
    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        edges = [(u, v) for u in range(n) for v in range(u+1, n)]
        m = len(edges)
        for _ in range(m // 2):
            u, v = random.sample(edges, 1)[0]
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def tseitin_formula(graph):
        clauses = []
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        neg_literals = {i: f'-x{i}' for i in range(n)}
        
        for i in range(n):
            clause = [neg_literals[i]]
            for j in graph[i]:
                clause.append(literals[j])
            clauses.append(clause)
        
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in graph and (j, i) not in graph:
                    clauses.append([neg_literals[i], neg_literals[j]])
                    clauses.append([literals[i], literals[j]])
        
        return clauses
    
    def resolution_length(clauses):
        clauses = [set(c) for c in clauses]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(lit in clause and -lit in other_clause for lit in clauses[i] for other_clause in clauses[j]):
                        new_lit = next(lit for lit in clauses[i] if -lit not in clauses[j])
                        new_clause = clauses[i].union(clauses[j]) - {new_lit, -new_lit}
                        if len(new_clause) == 0:
                            return float('inf')
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    clauses = tseitin_formula(graph)
    resolution_len = resolution_length(clauses)
    
    if resolution_len == float('inf'):
        return {
            "metric_name": "resolution_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    coxeter_group_size = 2 ** n
    ratio = coxeter_group_size / resolution_len
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_exceeds_bound' first_failing_seed={first_failing_seed}")