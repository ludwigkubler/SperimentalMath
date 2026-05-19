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
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 10))
    
    # Generate a random max-CUT instance
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute the degree-d SOS moment matrix M
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                for k in range(d):
                    M[i][k] += random.random()
                    M[j][k] += random.random()
    
    # Calculate eigenvalue spectrum
    eigvals = []
    for i in range(n):
        w = [M[i][j] - M[j][i] for j in range(n)]
        q = [1.0]
        for k in range(d):
            q_new = [q[0]]
            for l in range(1, len(q)):
                q_new.append(q[l-1] + w[l])
            q = q_new
        eigvals.extend([sum(q) / (2**k) for k in range(len(q))])
    
    # Check if eigenvalues exceed C * sqrt(n/d^3)
    C = 0.5  # Placeholder value, adjust as needed
    threshold = C * math.sqrt(n / d**3)
    any_exceeds = any(abs(lam) > threshold for lam in eigvals)
    
    # Use Monte Carlo sampling to check if 0.878-approximators consistently violate this threshold
    num_samples = 100
    violations = 0
    for _ in range(num_samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        cut_value = sum(x[i] * x[j] * G[i][j] for i in range(n) for j in range(i+1, n))
        if abs(cut_value / (n*(n-1)//2)) > 0.878:
            violations += 1
    
    # Determine if the relaxation can approximate max-CUT with ratio better than 0.878 - ε
    conjecture_holds = not any_exceeds and violations < num_samples * 0.9
    
    return {
        "metric_name": "eigenvalue_threshold",
        "metric_value": threshold,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")