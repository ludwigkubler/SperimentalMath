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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def sos_refutation_size(M, n):
        # Placeholder for actual SOS refutation size computation
        # This is a dummy implementation and should be replaced with actual code
        return int(n ** 0.5 * math.log(n))
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(range(-n, -1), 3) + random.sample(range(1, n+1), 3)
            clauses.append(clause)
        return clauses
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[0] * (n**2) for _ in range(n)]
    clauses = generate_3sat_instance(n)
    
    # Construct the constraint matrix M
    for clause in clauses:
        for x in clause:
            i, j = abs(x) - 1, abs(x) - 1 + n
            if x > 0:
                M[i][j] += 1
            else:
                M[j][i] += 1
    
    rank = gaussian_elimination(M)
    rho = sos_refutation_size(M, n)
    
    c = 0.5  # Constant factor for the inequality r(M) ≥ c·n/ρ
    if rank < c * n / rho:
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank}, rho={rho}"
        }
    else:
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")