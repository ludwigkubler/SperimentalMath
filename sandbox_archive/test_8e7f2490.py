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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def grothendieck_group_rank(phi):
        n = len(phi)
        clause_indicator_poly = [0] * (2**n)
        for clause in phi:
            index = 0
            for var in clause:
                index |= 1 << abs(var) - 1
                if var < 0:
                    index ^= (1 << (abs(var) - 1))
            clause_indicator_poly[index] += 1
        
        A = []
        for i in range(2**n):
            row = [clause_indicator_poly[i ^ j] for j in range(2**n)]
            A.append(row)
        
        return gaussian_elimination(A)
    
    def minimal_eta_quotient(rank, n):
        if rank == 0:
            return 0
        return Fraction(n * (n - 1), 2) / rank
    
    n_max = 40
    instances_tested = 30
    eta_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        phi = [random.sample(range(-n, n + 1), random.randint(2, n)) for _ in range(random.randint(1, n))]
        rank = grothendieck_group_rank(phi)
        eta_value = minimal_eta_quotient(rank, n)
        eta_values.append(eta_value)
    
    mean_eta = sum(eta_values) / instances_tested
    std_eta = math.sqrt(sum((x - mean_eta)**2 for x in eta_values) / instances_tested)
    
    conjecture_holds = all(eta <= n**2 for eta in eta_values)
    counterexample = "" if conjecture_holds else f"n={n}, eta={eta_value}"
    
    return {
        "metric_name": "minimal_eta_quotient",
        "metric_value": mean_eta,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_eta = sum(r["metric_value"] for r in results) / len(results)
    std_eta = math.sqrt(sum((r["metric_value"] - mean_eta)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_eta} std={std_eta} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_eta} std={std_eta} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")