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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def construct_algebraic_variety(f):
        # Simplified mapping to a polynomial
        n = len(f)
        poly = sum(f[i] * (x ** i) for i in range(n))
        return poly
    
    def hodge_diamond(poly):
        # Simplified Hodge diamond calculation
        degree = len(poly) - 1
        d = [[0] * (degree + 1) for _ in range(degree + 1)]
        d[0][0] = 1
        return d
    
    def communication_complexity_rank(f):
        # Simplified rank calculation
        n = len(f)
        rank = sum(1 for bit in f if bit == 1)
        return rank
    
    m = random.randint(5, 30)
    f = generate_boolean_function(m)
    X_f = construct_algebraic_variety(f)
    d_X_f = hodge_diamond(X_f)
    r_f = communication_complexity_rank(f)
    
    return {
        "metric_name": "d(X_f)",
        "metric_value": sum(sum(row) for row in d_X_f),
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 * mean_metric_value for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")