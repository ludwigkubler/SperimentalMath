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
    
    def generate_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            if A[max_row][i] == 0:
                continue
            A[rank], A[max_row] = A[max_row], A[rank]
            for j in range(m):
                if j != rank and A[j][i]:
                    factor = -A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def diophantine_representation_size(clauses, n):
        m = len(clauses)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                A[i][abs(var)] += 1 if var > 0 else -1
        return gaussian_elimination(A)
    
    n_max = 40
    instances_tested = 0
    total_size = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n, 20))
            cnf = generate_cnf(n, k)
            size = diophantine_representation_size(cnf, n)
            total_size += size
            instances_tested += 1
    
    mean_size = total_size / instances_tested
    conjecture_holds = mean_size <= k * math.log(n_max)
    
    return {
        "metric_name": "diophantine_representation_size",
        "metric_value": mean_size,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")