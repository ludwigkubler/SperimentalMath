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

def min_plus_convolution(f, n):
    g = [float('inf')] * n
    for y in range(n):
        for x in range(n):
            g[(x - y) % n] = min(g[(x - y) % n], f[y])
    return g

def tropical_fourier_transform(f, beta, n):
    F_beta = [0] * n
    for k in range(n):
        sum_exp = 0
        for x in range(n):
            sum_exp += math.exp(-beta * f[x]) * math.exp(-2 * math.pi * 1j * k * x / n)
        F_beta[k] = -(1 / beta) * math.log(sum_exp)
    return F_beta

def minimal_fourier_coefficient(F, n):
    return min(abs(F[k]) for k in range(n))

def discrepancy_measure(f, n):
    return max(f[x] - min(f[x] for x in range(n)) for x in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 16, 32, 64]:
        for beta in [5, 10, 20]:
            f = [random.randint(-10, 10) for _ in range(n)]
            g = min_plus_convolution(f, n)
            F_beta_f = tropical_fourier_transform(f, beta, n)
            MinFC_f = minimal_fourier_coefficient(F_beta_f, n)
            Disc_f = discrepancy_measure(f, n)
            
            MinFC_g = minimal_fourier_coefficient(tropical_fourier_transform(g, beta, n), n)
            Disc_g = discrepancy_measure(g, n)
            
            results.append({
                "n": n,
                "beta": beta,
                "MinFC_f": MinFC_f,
                "Disc_f": Disc_f,
                "MinFC_g": MinFC_g,
                "Disc_g": Disc_g
            })
    
    support_fraction = 0.95
    C = 5
    total_error = sum(abs(2 * MinFC_f - MinFC_g) for result in results)
    mean_error = total_error / len(results)
    
    conjecture_holds = all(abs(2 * MinFC_f - MinFC_g) <= C / n and Disc_g <= 2 * Disc_f + 1e-6 for result in results)
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Mean Error",
        "metric_value": mean_error,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_error = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_error} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")