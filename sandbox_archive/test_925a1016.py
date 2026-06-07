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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def topological_sort(clauses):
        graph = {var: set() for var in range(1, 2**n + 1)}
        indegree = {var: 0 for var in range(1, 2**n + 1)}
        
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    graph[lit].add(-lit)
                else:
                    graph[-lit].add(lit)
                indegree[abs(lit)] += 1
        
        queue = [var for var in range(1, 2**n + 1) if indegree[var] == 0]
        top_order = []
        
        while queue:
            node = queue.pop()
            top_order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        
        return top_order
    
    def resolution_width(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        width = 0
        
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    lit_i = clauses[i][0]
                    lit_j = -clauses[j][0]
                    if lit_i == lit_j:
                        new_clause = list(set(clauses[i] + clauses[j]) - {lit_i})
                        if new_clause not in clauses_set:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
            width += 1
        
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    top_order = topological_sort(cnf)
    orbit_space = set(tuple(sorted([abs(lit) for lit in clause])) for clause in cnf if all(lit in top_order for lit in clause))
    
    def entropy(probabilities):
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    probabilities = [orbit_space.count(orbit) / len(orbit_space) for orbit in orbit_space]
    h_orbit_space = entropy(probabilities)
    
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
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")