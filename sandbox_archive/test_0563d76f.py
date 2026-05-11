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

def fast_walsh_hadamard_transform(x):
    n = len(x)
    if n == 1:
        return x
    even = fast_walsh_hadamard_transform(x[0::2])
    odd = fast_walsh_hadamard_transform(x[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def discrepancy(G, n):
    def sample_discrepancy():
        s = random.sample(range(n), n // 2)
        t = [1 if i in s else -1 for i in range(n)]
        D_st = sum(G[i][j] * t[i] * t[j] for i in range(n) for j in range(i + 1, n))
        return abs(D_st)
    
    num_samples = 50
    total_discrepancy = sum(sample_discrepancy() for _ in range(num_samples))
    return total_discrepancy / num_samples

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    
    # Compute Fourier coefficients
    f_hat = [0] * (2 ** n)
    for S in range(2 ** n):
        sign = (-1) ** sum((S >> j) & 1 for j in range(n))
        f_hat[S] = sign * sum(A[i][j] for i in range(n) for j in range(i + 1, n) if (i ^ j) == S)
    
    # Compute discrepancy
    Δ = discrepancy(A, n)
    
    # Sum of absolute Fourier coefficients
    Σ_abs_f_hat = sum(abs(f_hat[S]) for S in range(2 ** n))
    
    # Check the conjecture
    if Δ == 0:
        counterexample = "discrepancy_zero"
        conjecture_holds = False
    else:
        ratio = Σ_abs_f_hat * Δ
        tolerance = 1e-6
        if abs(ratio - 2) < tolerance:  # Example threshold, adjust as needed
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = f"ratio={ratio}, expected≈2"
    
    return {
        "metric_name": "Σ|f̂(S)| * Δ",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.6f} std={std_ratio:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")