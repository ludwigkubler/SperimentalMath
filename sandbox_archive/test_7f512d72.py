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
    
    def geometric_entropy(f, n):
        Pr_f = [f(x)**2 for x in range(n)]
        H_f = -sum(p * math.log2(p) for p in Pr_f if p > 0)
        return H_f
    
    def spectral_excess(M):
        N = len(M)
        eigenvalues = []
        for i in range(N):
            v = [1] * N
            for _ in range(10):  # Power iteration method to approximate an eigenvector
                v = [sum(M[i][j] * v[j] for j in range(N)) for j in range(N)]
                v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            eigenvalues.append(v)
        lambda_max = max(abs(eigenvalue[0]) for eigenvalue in eigenvalues)
        lambda_min = min(abs(eigenvalue[-1]) for eigenvalue in eigenvalues)
        return lambda_max - (N - 1) * lambda_min
    
    def communication_complexity(M):
        N = len(M)
        k = math.ceil(math.log2(N))
        return math.floor(math.log2(1 + N * spectral_excess(M) / k)) - 1
    
    n = random.randint(5, 40)
    f = lambda x: random.choice([0, 1])
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    H_f = geometric_entropy(f, n)
    CC_M = communication_complexity(M)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": H_f,
        "instances_tested": 1,
        "conjecture_holds": H_f >= n,
        "counterexample": "" if H_f >= n else f"Geometric entropy {H_f} < {n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric_entropy_less_than_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")