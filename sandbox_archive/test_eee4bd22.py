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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def local_induction_dimension(f):
        n = len(f)
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    count += 1
        return count
    
    def partial_commutative_matrix(f):
        n = len(f)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = i
            for j in range(pivot_row + 1, n):
                if M[j][pivot_row] != 0:
                    M[pivot_row], M[j] = M[j], M[pivot_row]
                    break
            rank += 1
            for j in range(n):
                if j == pivot_row:
                    continue
                factor = M[j][pivot_row] / M[pivot_row][pivot_row]
                for k in range(n):
                    M[j][k] -= factor * M[pivot_row][k]
        return rank
    
    n = 10  # Start with a small size and increase if necessary
    while True:
        f = generate_random_boolean_function(n)
        lnd_f = local_induction_dimension(f)
        if lnd_f <= 40:
            break
        n += 5
    
    M_f = partial_commutative_matrix(f)
    rank_M_f = matrix_rank(M_f)
    
    metric_value = Fraction(rank_M_f, math.log(n)**2 * lnd_f).limit_denominator()
    conjecture_holds = abs(metric_value - Fraction(1)) <= Fraction(10, 100)
    counterexample = "" if conjecture_holds else f"n={n}, rank(M_f)={rank_M_f}, log^2(n)*lnd(f)={math.log(n)**2 * lnd_f}"
    
    return {
        "metric_name": "Rank Ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")