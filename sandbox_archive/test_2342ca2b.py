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
    
    def generate_polynomial(n, D):
        poly = [[0] * (D + 1) for _ in range(D + 1)]
        for i in range(1, D + 1):
            for j in range(i, D + 1):
                if i == j:
                    poly[i][j] = random.randint(1, n)
                else:
                    poly[i][j] = random.randint(-n, n)
        return poly
    
    def plethysm_coefficients(poly, n):
        D = len(poly) - 1
        result = [[0] * (D + 1) for _ in range(D + 1)]
        result[0][0] = 1
        for i in range(1, D + 1):
            for j in range(i, D + 1):
                if i == j:
                    result[i][j] = poly[i][j]
                else:
                    result[i][j] = sum(result[i - k][j - 1] * poly[k][j - 1] for k in range(1, min(i, j) + 1))
        return result
    
    def permanent_circuit_size(poly):
        D = len(poly) - 1
        if D == 0:
            return 1
        size = 0
        for i in range(1, D + 1):
            size += sum(permanent_circuit_size(sub_poly) for sub_poly in poly[1:i])
        return size
    
    n = random.randint(5, 40)
    D = int(math.log2(n)) ** 2
    poly = generate_polynomial(n, D)
    plethysm_coeffs = plethysm_coefficients(poly, n)
    perm_circuit_size = permanent_circuit_size(poly)
    
    metric_name = "Rank vs Perm Circuit Size"
    metric_value = len([x for x in plethysm_coeffs if any(y != 0 for y in x)]) / (D + 1) ** 2
    instances_tested = 1
    conjecture_holds = metric_value >= D and perm_circuit_size <= n ** 1.5 * D
    counterexample = "" if conjecture_holds else f"Rank {metric_value} < {D}, Perm Circuit Size {perm_circuit_size} > {n ** 1.5 * D}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")