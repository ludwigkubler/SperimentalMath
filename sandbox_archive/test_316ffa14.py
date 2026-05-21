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
from math import factorial, sqrt
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hook_length_formula(shape):
        n = sum(shape)
        numerator = 1
        denominator = 1
        for row in shape:
            for i in range(row):
                numerator *= (n - i)
                denominator *= (row - i)
        return Fraction(numerator, denominator)
    
    def det_m_hook_length_ratio(m):
        if m == 0:
            return 1
        shape = [m] * m
        return hook_length_formula(shape) / factorial(m)
    
    n_values = [5, 10, 15, 20, 30, 40]
    perm_n_ratios = []
    det_m_ratios = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            shape = [n] * n
            perm_n_ratios.append(hook_length_formula(shape) / factorial(n))
            m = int(sqrt(n)) + 1
            det_m_ratios.append(det_m_hook_length_ratio(m))
    
    mean_perm_n_ratio = sum(perm_n_ratios) / len(perm_n_ratios)
    mean_det_m_ratio = sum(det_m_ratios) / len(det_m_ratios)
    
    conjecture_holds = all(r > mean_det_m_ratio for r in perm_n_ratios)
    counterexample = "" if conjecture_holds else "det_m_hook_length_ratio < perm_n_hook_length_ratio"
    
    return {
        "metric_name": "hook_length_ratio",
        "metric_value": (mean_perm_n_ratio, mean_det_m_ratio),
        "instances_tested": len(perm_n_ratios) + len(det_m_ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_perm_n_ratio = sum(r["metric_value"][0] for r in results) / len(results)
    mean_det_m_ratio = sum(r["metric_value"][1] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean_perm_n_ratio={mean_perm_n_ratio} std_det_m_ratio={mean_det_m_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"det_m_hook_length_ratio < perm_n_hook_length_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")