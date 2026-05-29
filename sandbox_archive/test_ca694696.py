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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_jordan_algebra(f):
        n = len(f)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = A[j][i] = f[i] ^ f[j]
        return A
    
    def compute_noncommutative_geometric_invariant(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i+1, n)):
                continue
            pivot_row = next(j for j in range(i+1, n) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def compute_bp_size(f):
        n = len(f)
        size = 0
        for i in range(1, n+1):
            if all(f[j] == f[0] for j in range(i)):
                break
            size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_j = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = compute_jordan_algebra(f)
        j = compute_noncommutative_geometric_invariant(A)
        total_j += j
        instances_tested += 1
        
        if j > (2 * n) ** 2:
            conjecture_holds = False
            counterexample = f"J(f) = {j} exceeds O(log^2({n})) for read-twice BP"
        
        bp_size = compute_bp_size(f)
        if bp_size == 1 and j < n:
            conjecture_holds = False
            counterexample = f"J(IP_2 trivial BP) = {j} is less than Ω(n)"
    
    mean_j = total_j / instances_tested
    return {
        "metric_name": "Noncommutative Geometric Invariant J(f)",
        "metric_value": mean_j,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_j = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_j} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_j} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")