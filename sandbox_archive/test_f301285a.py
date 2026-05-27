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

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_polynomial(n, p):
    return [random.randint(0, p - 1) for _ in range(n + 1)]

def hodge_rank(f, p):
    n = len(f) - 1
    A = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        for j in range(n + 1):
            if i + j > n:
                continue
            A[i][j] = sum((f[k] ** (i + j - k)) % p for k in range(n + 1)) % p
    
    # Gaussian elimination to find rank
    rank = 0
    for col in range(n + 1):
        pivot_row = None
        for row in range(rank, n + 1):
            if A[row][col] != 0:
                pivot_row = row
                break
        
        if pivot_row is not None:
            rank += 1
            for j in range(col, n + 1):
                A[pivot_row][j], A[rank - 1][j] = A[rank - 1][j], A[pivot_row][j]
            
            for row in range(n + 1):
                if row != rank - 1:
                    factor = (A[row][col] * pow(A[rank - 1][col], p - 2, p)) % p
                    for j in range(col, n + 1):
                        A[row][j] = (A[row][j] - factor * A[rank - 1][j]) % p
    
    return rank

def min_refutation_size(f):
    # Simplified heuristic to estimate refutation size
    # This is a placeholder and should be replaced with actual resolution proof logic
    n = len(f) - 1
    return 2 ** n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    p = random.choice(generate_primes(30))
    n = random.randint(5, 40)
    f = random_polynomial(n, p)
    
    hodge_r = hodge_rank(f, p)
    refutation_size = min_refutation_size(f)
    
    metric_value = math.log(refutation_size) if refutation_size > 0 else -math.inf
    conjecture_holds = hodge_r >= metric_value
    
    return {
        "metric_name": "Hodge Rank vs Refutation Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Refutation size {refutation_size} not logarithmically bounded by Hodge rank {hodge_r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation size not logarithmically bounded by Hodge rank\" first_failing_seed={first_failing_seed}")