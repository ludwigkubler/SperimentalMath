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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] = -clause[0]
            if random.choice([True, False]):
                clause[1] = -clause[1]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf, n):
        m = len(cnf)
        M = [[0] * n for _ in range(m)]
        for i, (x, y) in enumerate(cnf):
            x -= 1
            y -= 1
            M[i][x] = 1
            M[i][y] = -1
        return M
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(M[i][j]) > abs(M[i_max][j]):
                    i_max = i
            if M[i_max][j] == 0:
                continue
            M[rank], M[i_max] = M[i_max], M[rank]
            for i in range(m):
                if i != rank:
                    factor = M[i][j] / M[rank][j]
                    for k in range(n):
                        M[i][k] -= factor * M[rank][k]
            rank += 1
        return rank
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                return abs(clause[0])
            for other in cnf:
                if not any(abs(lit) == abs(other[0]) and lit != other[0] for lit in clause):
                    continue
                new_clause = [x for x in other if x not in clause]
                if len(new_clause) == 1:
                    return abs(new_clause[0])
                if tuple(sorted(new_clause)) in seen:
                    continue
                seen.add(tuple(sorted(new_clause)))
                queue.append(new_clause)
        return float('inf')
    
    n = random.randint(5, 40)
    m = random.randint(n + 1, n * (n + 1) // 2)
    cnf = generate_cnf(n, m)
    M = incidence_matrix(cnf, n)
    mtr = gaussian_elimination(M)
    w = resolution_width(cnf)
    
    if mtr > 1.5 * w:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mtr > 1.5 * w"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": mtr / w if w != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mtr > 1.5 * w\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")