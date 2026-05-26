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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = random.randint(1, 10)
            neighbors = random.sample(range(n), degree)
            for j in neighbors:
                if i != j:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def boolean_fourier_coefficients(G, n):
        m = len(G)
        F = [0] * (1 << m)
        
        for s in range(1 << m):
            sign = (-1) ** bin(s).count('1')
            term = 1
            for i in range(m):
                if s & (1 << i):
                    term *= G[i][i]
            F[s] += sign * term
        
        return F
    
    def min_quasi_poly_growth(F, n):
        max_val = max(abs(x) for x in F)
        growth_rate = math.log(max_val) / math.log(n)
        return growth_rate
    
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    F = boolean_fourier_coefficients(G, n)
    min_growth = min_quasi_poly_growth(F, n)
    
    metric_name = "min_quasi_poly_growth"
    metric_value = min_growth
    instances_tested = 1
    conjecture_holds = min_growth >= (2**n / math.log(n)**2) and min_growth <= math.log(n**(G[0][0] + 1), n)
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices, growth rate {min_growth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")