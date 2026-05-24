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
    
    def generate_random_polynomial(n):
        coefficients = [random.randint(0, 10) for _ in range(n + 1)]
        return coefficients
    
    def compute_BP_readTwice_tensor_width(P):
        n = len(P)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if P[i][j] != 0:
                    width += 1
        return width
    
    n = random.randint(5, 40)
    r = random.randint(1, min(n // 2, 10))
    
    # Generate a read-twice BP P of size n
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    P = [row[:i] + row[i+1:] for i, row in enumerate(P)]
    
    # Compute the BP_readTwice tensor width ρ(P)
    rho_P = compute_BP_readTwice_tensor_width(P)
    
    # Construct a quadratic form Q based on the independent linear forms of P
    Q = [[0] * n for _ in range(n)]
    for i in range(r):
        poly = generate_random_polynomial(n)
        for j in range(n):
            Q[j][j] += poly[j]
    
    # Compute the BP_readTwice tensor width ρ(Q)
    rho_Q = compute_BP_readTwice_tensor_width(Q)
    
    # Evaluate the upper bound on ρ(Q) using the formula O(n^2r log(r))
    upper_bound = n**2 * r * math.log(r)
    
    return {
        "metric_name": "BP_readTwice tensor width",
        "metric_value": rho_Q,
        "instances_tested": 1,
        "conjecture_holds": abs(rho_Q - rho_P) <= upper_bound,
        "counterexample": "" if rho_Q <= upper_bound else f"rho(Q)={rho_Q} > {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len(results) / len(seeds)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")