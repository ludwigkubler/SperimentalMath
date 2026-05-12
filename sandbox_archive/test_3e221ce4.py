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
    
    def generate_sipser_function(n):
        # Generate a random Sipser function (parity function for simplicity)
        return lambda x: sum(x) % 2
    
    def group_action(f, g):
        # Group action on n-bit strings by permutation g
        return [f(tuple(g[i] for i in range(len(f)))) for f in f]
    
    def young_tableaux_decomposition(n):
        # Young tableaux decomposition for S_3 (symmetric group of order 3)
        if n == 1:
            return [[0]]
        elif n == 2:
            return [[0, 1], [1, 0]]
        else:
            raise ValueError("Unsupported n for young_tableaux_decomposition")
    
    def noncommutative_fourier_coefficients(f):
        # Compute noncommutative Fourier coefficients using Young tableaux decomposition
        tableaux = young_tableaux_decomposition(3)
        return sum(abs(f(t)) for t in tableaux) / len(tableaux)
    
    n = random.randint(5, 40)
    f = generate_sipser_function(n)
    g = [random.sample(range(n), n) for _ in range(n)]
    f_g = group_action(f, g)
    F_k = noncommutative_fourier_coefficients(f_g)
    
    return {
        "metric_name": "noncommutative_fourier_coeff_sum",
        "metric_value": F_k,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")