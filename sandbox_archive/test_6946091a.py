# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def permutation_multiply(p1, p2):
    return tuple(p1[p2[i]] for i in range(len(p1)))

def inversions(perm):
    count = 0
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                count += 1
    return count

def barrington_compile(d):
    n = 2 ** d
    sigma = (1, 2, 3, 4, 5)
    B = []
    for k in range(4 ** d):
        layers = [sigma]
        for _ in range(k):
            if random.choice([0, 1]) == 0:
                layers.append(permutation_multiply(sigma, sigma))
            else:
                layers.append(permutation_multiply(sigma, (5, 1, 2, 3, 4)))
        B.append(layers)
    return B

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 16
    L = 256
    instances_tested = 0
    sigma_squared_sum = 0
    
    for _ in range(50):
        x = tuple(random.randint(0, 1) for _ in range(n))
        pi_k_values = []
        for k in range(L + 1):
            layers = barrington_compile(int(k**(1/4)))
            pi_k = (1, 2, 3, 4, 5)
            for layer in layers:
                if k == 0:
                    pi_k = layer
                else:
                    pi_k = permutation_multiply(pi_k, layer[k % len(layer)])
            pi_k_values.append(inversions(pi_k))
        
        mu_x = sum(pi_k_values) / L
        variance = sum((pi_k - mu_x)**2 for pi_k in pi_k_values) / L
        sigma_squared_sum += variance
        instances_tested += 1
    
    mean_sigma_squared = sigma_squared_sum / instances_tested
    conjecture_holds = (mean_sigma_squared <= 4 * d and mean_sigma_squared >= Fraction(1, 8))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "sigma_squared",
        "metric_value": mean_sigma_squared,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_sigma_squared = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = (sum((r["metric_value"] - mean_sigma_squared)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_sigma_squared} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")