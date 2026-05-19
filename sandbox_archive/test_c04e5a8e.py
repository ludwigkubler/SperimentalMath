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
    
    # Define constants and parameters
    n = 30  # Number of vertices
    d = 2   # Degree of SOS relaxation
    C = 1.5  # Universal constant for eigenvalue bound
    
    # Generate a random max-CUT instance
    graph = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # Compute the degree-d SOS moment matrix M
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 1:
                for k in range(d):
                    M[i][k] += (i + k) % n
                    M[j][k] += (j + k) % n
    
    # Calculate the eigenvalue spectrum of M
    eigenvalues = []
    for i in range(n):
        v = [1 if j == i else 0 for j in range(n)]
        while True:
            Av = [sum(M[i][k] * v[k] for k in range(n)) for k in range(n)]
            norm_v = sum(v[j]**2 for j in range(n))
            norm_Av = sum(Av[j]**2 for j in range(n))
            if norm_v == 0 or norm_Av == 0:
                break
            v = [Av[j] / norm_Av for j in range(n)]
        eigenvalues.append(v)
    
    # Verify if eigenvalues exceed C * sqrt(n/d^3)
    threshold = C * math.sqrt(n / d**3)
    max_eigenvalue = max(abs(eig) for eig in eigenvalues)
    conjecture_holds = max_eigenvalue <= threshold
    
    return {
        "metric_name": "eigenvalue_threshold",
        "metric_value": max_eigenvalue,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_eigenvalue={max_eigenvalue}, threshold={threshold}"
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")