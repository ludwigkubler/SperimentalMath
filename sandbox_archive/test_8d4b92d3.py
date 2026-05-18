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
    
    def perm_mult(p1, p2):
        return tuple((p1[i] - 1 for i in p2))
    
    def inversions(perm):
        count = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    count += 1
        return count
    
    def barrington_compile(d: int) -> list:
        n = 2 ** d
        L = 4 ** d
        layers = []
        for k in range(1, L + 1):
            i_k = random.sample(range(n), 5)
            g_k0 = (i_k[0], i_k[1], i_k[2], i_k[3], i_k[4])
            g_k1 = perm_mult(g_k0, (1, 2, 3, 4, 5))
            layers.append((i_k, g_k0, g_k1))
        return layers
    
    def compute_sigma_squared(layers):
        n = len(layers)
        L = len(layers)
        mu_x = [0] * n
        for k in range(n):
            mu_x[k] = sum(inversions(perm_mult(g[:k+1], (i[0], i[1], i[2], i[3], i[4]))) for i, g0, g1 in layers) / L
        
        sigma_squared = 0
        for k in range(n):
            pi_k = (i[0], i[1], i[2], i[3], i[4])
            sigma_squared += sum((inversions(perm_mult(pi_k[:k+1], (i[0], i[1], i[2], i[3], i[4]))) - mu_x[k]) ** 2 for i, g0, g1 in layers) / L
        
        return sigma_squared
    
    depths = [1, 2, 3, 4]
    results = []
    
    for d in depths:
        B = barrington_compile(d)
        sigma_squared = compute_sigma_squared(B)
        results.append({
            "metric_name": "sigma_squared",
            "metric_value": sigma_squared,
            "instances_tested": len(B),
            "conjecture_holds": sigma_squared <= 4 * d and sigma_squared >= 1 / 8,
            "counterexample": "" if sigma_squared <= 4 * d and sigma_squared >= 1 / 8 else f"sigma_squared={sigma_squared}"
        })
    
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["trials"])
    
    sigma_squared_values = [r["metric_value"] for r in all_results]
    conjecture_holds = all(r["conjecture_holds"] for r in all_results)
    
    mean_sigma_squared = sum(sigma_squared_values) / len(sigma_squared_values)
    std_deviation = math.sqrt(sum((x - mean_sigma_squared) ** 2 for x in sigma_squared_values) / len(sigma_squared_values))
    support_fraction = 1.0 if conjecture_holds else len([r for r in all_results if not r["conjecture_holds"]]) / len(all_results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_sigma_squared} std={std_deviation} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in all_results):
        first_failing_seed = next(s for s, r in enumerate(all_results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{all_results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")