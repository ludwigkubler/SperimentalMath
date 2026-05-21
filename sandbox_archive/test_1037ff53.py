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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def hook_length_formula(shape):
        total = 1
        for row in shape:
            for cell in row:
                total /= (cell + len(row) - row.index(cell))
        return total
    
    def young_diagram_hook_lengths(n):
        if n == 0:
            return [[]]
        diagrams = []
        for i in range(1, n + 1):
            subdiagrams = young_diagram_hook_lengths(n - i)
            for subdiag in subdiagrams:
                new_diag = [row[:] for row in subdiag]
                new_diag.append([i] * (n - i))
                diagrams.append(new_diag)
        return diagrams
    
    def perm_n_hook_length_ratio(n):
        shape = [[i + 1 for _ in range(i)] for i in range(1, n + 1)]
        return hook_length_formula(shape) / factorial(n)
    
    def det_m_hook_length_ratio(m):
        if m == 0:
            return 1
        shape = [[m] * m]
        return hook_length_formula(shape) / factorial(m)
    
    n = random.randint(5, 40)
    perm_n_ratio = perm_n_hook_length_ratio(n)
    det_m_ratios = [det_m_hook_length_ratio(m) for m in range(1, int(n ** 1.5))]
    
    metric_name = "hook_length_ratio"
    metric_value = sum(det_m_ratios) / len(det_m_ratios)
    instances_tested = len(det_m_ratios)
    conjecture_holds = perm_n_ratio > metric_value
    counterexample = "" if conjecture_holds else f"perm_{n} has H(f)={perm_n_ratio}, det_{len(det_m_ratios)} has H(f)={metric_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")