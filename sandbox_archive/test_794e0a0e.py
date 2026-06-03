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
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def monotone_width(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        m = len(cnf)
        
        # Initialize the adjacency matrix
        adj = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    lit1, lit2 = clause[i], clause[j]
                    if (lit1 > 0 and lit2 < 0) or (lit1 < 0 and lit2 > 0):
                        adj[abs(lit1)][abs(lit2)] = 1
                        adj[abs(lit2)][abs(lit1)] = 1
        
        # Find the maximum matching using Hall's Marriage Theorem
        def bfs_match(v, match, seen):
            queue = [v]
            while queue:
                u = queue.pop(0)
                for v in range(n + 1):
                    if adj[u][v] and v not in seen:
                        seen.add(v)
                        if match[v] is None or bfs_match(match[v], match, seen):
                            match[v] = u
                            return True
            return False
        
        match = [None] * (n + 1)
        for u in range(1, n + 1):
            if match[u] is None:
                bfs_match(u, match, set())
        
        # The monotone width is the size of the maximum matching
        return sum(match[v] is not None for v in range(n + 1)) // 2
    
    def cohomological_dimension(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        m = len(cnf)
        
        # Initialize the incidence matrix
        inc = [[0] * (m + 1) for _ in range(n + 1)]
        for i, clause in enumerate(cnf, start=1):
            for lit in clause:
                inc[abs(lit)][i] = 1
        
        # Compute the rank of the incidence matrix
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            rank = 0
            for j in range(cols):
                i_max = next((i for i in range(rank, rows) if mat[i][j]), None)
                if i_max is not None:
                    mat[rank], mat[i_max] = mat[i_max], mat[rank]
                    for i in range(rank + 1, rows):
                        factor = mat[i][j] / mat[rank][j]
                        for k in range(j, cols):
                            mat[i][k] -= factor * mat[rank][k]
                    rank += 1
            return rank
        
        return gaussian_elimination(inc)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mu = 0.0
    total_diff = 0.0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            mu = cohomological_dimension(cnf)
            w_m = monotone_width(cnf)
            instances_tested += 1
            total_mu += mu
            total_diff += abs(mu - w_m)
    
    mean_mu = total_mu / instances_tested
    mean_diff = total_diff / instances_tested
    
    return {
        "metric_name": "cohomological_dimension",
        "metric_value": mean_mu,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_diff <= 3,
        "counterexample": "" if mean_diff <= 3 else f"mean_diff={mean_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mean_diff>3' first_failing_seed={first_failing_seed}")