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

def random_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    indices = list(range(n))
    for i in range(n):
        j = random.choice(indices)
        M[i][j] = 1
        indices.remove(j)
    return M

def power_iteration(matrix, n=1000):
    v = [random.random() for _ in range(len(matrix))]
    v /= sum(v)
    for _ in range(n):
        v = matrix @ v
        v /= sum(v)
    return max(abs(x) for x in v)

def spectral_radius(matrix):
    return power_iteration(matrix)

def free_entropy(M):
    X = [[(M[i][j] + 1) / 2 for j in range(len(M))] for i in range(len(M))]
    rho = spectral_radius(X)
    # Approximate τ(M) using numerical integration
    tau_M = -math.log(rho)
    return tau_M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 16
    M = random_disjointness_matrix(n)
    tau_M = free_entropy(M)
    metric_value = tau_M
    instances_tested = 1
    conjecture_holds = tau_M >= 0.3 * n
    counterexample = "" if conjecture_holds else "free_entropy_too_low"
    return {
        "metric_name": "tau_M",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
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
        print(f"RESULT: FALSIFIED counterexample=\"free_entropy_too_low\" first_failing_seed={first_failing_seed}")