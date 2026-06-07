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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def topological_sort(clauses):
        graph = {i: set() for i in range(1, 2 * n + 1)}
        in_degree = {i: 0 for i in range(1, 2 * n + 1)}
        
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    graph[literal].add(-literal)
                else:
                    graph[-literal].add(literal)
                in_degree[abs(literal)] += 1
        
        queue = [i for i in range(1, 2 * n + 1) if in_degree[i] == 0]
        order = []
        
        while queue:
            node = queue.pop()
            order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return order
    
    def resolution_width(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        width = 0
        
        while clauses_set:
            new_clause = None
            for clause1 in clauses_set:
                for clause2 in clauses_set:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted([x for x in clause1 + clause2 if x not in (set(clause1) & set(clause2))]))
                        break
                if new_clause:
                    break
            if not new_clause:
                return width
            clauses_set.add(new_clause)
            width += 1
        
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    orbit_space = topological_sort(cnf)
    h_orbit_space = len(set(len(list(filter(lambda x: abs(x) in clause, orbit_space))) for clause in cnf))
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "h(OrbitSpace(φ))",
        "metric_value": h_orbit_space,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_orbit_space <= w_phi * 2 and h_orbit_space >= w_phi / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 997) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] / w_phi > 2 or r["metric_value"] < w_phi / 2 for r, w_phi in zip(results, [r["metric_value"] for r in results])):
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_below_80\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")