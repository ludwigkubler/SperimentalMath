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
    
    def walsh_hadamard_transform(f):
        n = len(f)
        for s in range(1, n):
            for i in range(n // (2 ** s)):
                for j in range(2 ** s):
                    f[i * 2 ** s + j], f[i * 2 ** s + j + 2 ** (s - 1)] = (
                        f[i * 2 ** s + j] + f[i * 2 ** s + j + 2 ** (s - 1)],
                        f[i * 2 ** s + j] - f[i * 2 ** s + j + 2 ** (s - 1)]
                    )
        return f
    
    def disjointness_communication_complexity(n):
        # Generate a random 3-CNF instance
        clauses = []
        for _ in range(3 * n):
            clause = [random.choice([-1, 1]) * random.randint(0, n - 1) for _ in range(3)]
            while len(set(clause)) != 3:
                clause = [random.choice([-1, 1]) * random.randint(0, n - 1) for _ in range(3)]
            clauses.append(clause)
        
        # Compute the Fourier coefficients
        f = [0] * (2 ** n)
        for x in range(2 ** n):
            sign = (-1) ** sum(x >> i & 1 for clause in clauses if any(lit == -x >> i & 1 or lit == x >> i & 1 for lit in clause))
            f[x] += sign
        
        # Compute the sum of absolute values of Fourier coefficients
        sum_abs_F_k = sum(abs(coeff) for coeff in f)
        
        # Estimate communication complexity (simplified heuristic)
        return math.ceil(math.sqrt(sum_abs_F_k))
    
    n = 40
    cc = disjointness_communication_complexity(n)
    sum_abs_F_k = sum(abs(coeff) for coeff in walsh_hadamard_transform([f(x, y) for x in range(2 ** n) for y in range(2 ** n)]))
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": cc >= math.sqrt(sum_abs_F_k),
        "counterexample": "" if cc >= math.sqrt(sum_abs_F_k) else f"Graph with n={n}, CC={cc}, sum_abs_F_k={sum_abs_F_k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")