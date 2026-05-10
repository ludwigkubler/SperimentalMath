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
    
    def generate_bp(n, read_twice):
        if n <= 0 or not isinstance(n, int):
            return None
        bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if read_twice:
            for i in range(n):
                for j in range(n):
                    bp[i][j] ^= bp[j][i]
        return bp
    
    def noncommutative_fourier_transform(bp):
        n = len(bp)
        fourier_coeffs = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    fourier_coeffs[i][j] += bp[(i + k) % n][(j + k) % n]
        return fourier_coeffs
    
    def max_abs_coefficient(fourier_coeffs):
        return max(abs(coeff) for row in fourier_coeffs for coeff in row)
    
    n = 40
    read_twice_bp = generate_bp(n, True)
    read_once_bp = generate_bp(n, False)
    
    if read_twice_bp is None or read_once_bp is None:
        return {
            "metric_name": "noncommutative_fourier_coefficient",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    read_twice_max_coeff = max_abs_coefficient(noncommutative_fourier_transform(read_twice_bp))
    read_once_max_coeff = max_abs_coefficient(noncommutative_fourier_transform(read_once_bp))
    
    return {
        "metric_name": "noncommutative_fourier_coefficient",
        "metric_value": read_twice_max_coeff / read_once_max_coeff,
        "instances_tested": 1,
        "conjecture_holds": read_twice_max_coeff >= n and read_once_max_coeff <= math.log(n),
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")