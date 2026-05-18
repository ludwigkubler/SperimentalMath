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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

# Constants
C1 = 4
c2 = Fraction(1, 8)

# Helper functions
def permutation_multiply(p1, p2):
    return tuple(p1[p2[i]] for i in range(len(p1)))

def barrington_compile(d):
    sigma = (1, 2, 3, 4, 5)
    layers = [sigma]
    for _ in range(4**d - 1):
        layers.append(permutation_multiply(sigma, sigma))
    return layers

def compute_sigma_squared(layers, n):
    L = len(layers)
    mu_x = [0] * (2**n)
    for x in range(2**n):
        pi = layers[0]
        for k in range(1, L):
            pi = permutation_multiply(pi, layers[k][x & 1])
        mu_x[x] = sum(layers[k].count(pi) for k in range(L)) / L
    sigma_squared = 0
    for x in range(2**n):
        pi = layers[0]
        for k in range(1, L):
            pi = permutation_multiply(pi, layers[k][x & 1])
            sigma_squared += (1/L) * ((layers[k].count(pi) - mu_x[x]) ** 2)
    return sigma_squared

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2**d for d in range(1, 5)]
    results = []
    
    for n in n_values:
        layers = barrington_compile(int(n**(1/4)))
        L = len(layers)
        sigma_squared = compute_sigma_squared(layers, n)
        
        results.append({
            "n": n,
            "L": L,
            "sigma_squared": sigma_squared
        })
    
    mean_sigma_squared = sum(result["sigma_squared"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["sigma_squared"] - mean_sigma_squared) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(sigma_squared <= C1 * d and sigma_squared >= c2 for n, L, sigma_squared in results for d in range(1, 5))
    counterexample = "" if conjecture_holds else "sigma_squared out of bounds"
    
    return {
        "metric_name": "sigma_squared",
        "metric_value": mean_sigma_squared,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")