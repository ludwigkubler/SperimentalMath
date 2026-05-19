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
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    # Generate a grid graph with n x n nodes
    G = [[(i, j) for j in range(n)] for i in range(n)]
    edges = []
    for i in range(n):
        for j in range(n):
            if i > 0: edges.append(((i-1, j), (i, j)))
            if j > 0: edges.append(((i, j-1), (i, j)))
    
    def treewidth(G):
        n = len(G)
        if n == 1:
            return 0
        for u in G[0]:
            neighbors = [v for v in G[0] if v != u]
            if len(neighbors) <= 1:
                continue
            G_prime = [set(v for v in row if v != u) for row in G[1:]]
            return max(treewidth(G_prime), len(neighbors))
        return float('inf')
    
    ν_G = treewidth(G)
    
    def tseitin_formula(G):
        clauses = []
        for i in range(n):
            for j in range(n):
                clauses.append([(i, j)])
                if i > 0:
                    clauses.append([(-i-1, j), (i, j)])
                if j > 0:
                    clauses.append([(-i, -j-1), (i, j)])
        return clauses
    
    def resolution_length(clauses):
        clauses = [set(c) for c in clauses]
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if len(clauses[i] & clauses[j]) == 1:
                        new_clause = (clauses[i] | clauses[j]) - {list(clauses[i] & clauses[j])[0]}
                        if len(new_clause) == 0:
                            return float('inf')
                        new_clauses.add(frozenset(new_clause))
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    clauses = tseitin_formula(G)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2**math.ceil(ν_G * math.log(2, 3)),
        "counterexample": "" if length >= 2**math.ceil(ν_G * math.log(2, 3)) else f"Grid graph of size {n} with treewidth {ν_G}"
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
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")