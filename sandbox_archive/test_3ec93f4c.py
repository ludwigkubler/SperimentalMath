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
    
    def hamming_distance(x, y):
        return sum(1 for a, b in zip(x, y) if a != b)
    
    def linear_programming(metric, r):
        n = len(metric)
        c = [-1] * n
        A = []
        b = []
        
        for i in range(n):
            row = [0] * n
            for j in range(n):
                if hamming_distance(i, j) <= r:
                    row[j] = 1
            A.append(row)
            b.append(1)
        
        # Solve the LP dual using Gaussian elimination
        A = [row + [c[i]] for i, row in enumerate(A)]
        n = len(A)
        m = len(A[0])
        pivot_col = 0
        
        for i in range(n):
            if A[i][pivot_col] == 0:
                for j in range(i+1, n):
                    if A[j][pivot_col] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    pivot_col += 1
                    continue
            
            for j in range(n):
                if i != j and A[j][pivot_col] != 0:
                    factor = -A[j][pivot_col] / A[i][pivot_col]
                    A[j] = [A[j][k] + factor * A[i][k] for k in range(m)]
        
        y = [row[-1] for row in A if all(row[k] == 0 for k in range(n))]
        return sum(y)

    def asdim(X):
        n = len(X)
        metric = [[hamming_distance(i, j) for j in X] for i in X]
        max_multiplicity = 0
        for r in range(1, n+1):
            multiplicity = linear_programming(metric, r)
            if multiplicity > max_multiplicity:
                max_multiplicity = multiplicity
        return max_multiplicity

    def generate_PAR_n(n):
        base = [tuple(i) for i in itertools.product([0, 1], repeat=n)]
        X_0 = [x for x in base if sum(x) % 2 == 0]
        X_1 = [x for x in base if sum(x) % 2 != 0]
        return X_0 + X_1

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        X = generate_PAR_n(n)
        asdim_value = asdim(X)
        results.append(asdim_value)
    
    a, b = polyfit(range(len(results)), results, 1)
    mean_asdim = sum(results) / len(results)
    std_asdim = math.sqrt(sum((x - mean_asdim) ** 2 for x in results) / len(results))
    
    conjecture_holds = a >= 0.8 and b >= -3
    counterexample = "" if conjecture_holds else f"asdim(X_{n_values[-1]}) = {mean_asdim}, expected at least {n_values[-1] - 3}"
    
    return {
        "metric_name": "asdim",
        "metric_value": mean_asdim,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_asdim = sum(results) / len(results)
    std_asdim = math.sqrt(sum((x - mean_asdim) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= seeds[-1] - 3) / len(results)
    
    if all(r >= seeds[-1] - 3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_asdim} std={std_asdim} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_asdim} std={std_asdim} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r < seeds[-1] - 3)
        print(f"RESULT: FALSIFIED counterexample='asdim(X_{seeds[-1]}) = {results[first_failing_seed]}, expected at least {seeds[-1] - 3}' first_failing_seed={first_failing_seed}")