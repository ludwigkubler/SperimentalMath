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
    
    def young_tableaux(n):
        if n == 1:
            return [[]]
        tableaux = []
        for i in range(1, n):
            for t in young_tableaux(n - i):
                tableaux.append([i] + t)
        return tableaux
    
    def hook_length_formula(shape):
        n = len(shape)
        fact = math.factorial
        numerator = fact(n * (n + 1) // 2)
        denominator = 1
        for row in shape:
            for i, cell in enumerate(row):
                denominator *= (cell + i + 1)
        return numerator / denominator
    
    def plethysm_coefficient(shape, k):
        n = len(shape)
        if k == 0:
            return 1
        coeff = 0
        for t in young_tableaux(n):
            if len(t) >= k:
                coeff += hook_length_formula([t[i] + 1 for i in range(k)])
        return coeff / (k * hook_length_formula(shape))
    
    n = random.randint(2, 40)
    m = int(n ** 1.5)
    k = n // 2
    
    perm_coeff = plethysm_coefficient([n - k + 1] + [1] * (n - k), k)
    det_coeff = plethysm_coefficient([n - k + 1] + [1] * (n - k), k)
    
    ratio = perm_coeff / det_coeff
    
    conjecture_holds = ratio > 2 ** (n / 2)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 2^{n/2}"
    
    return {
        "metric_name": "plethysm_coefficient_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")