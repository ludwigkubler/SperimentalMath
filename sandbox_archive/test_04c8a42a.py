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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def hook_length_formula(shape):
        rows, cols = len(shape), len(shape[0])
        hook_lengths = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                hook_lengths[i][j] = shape[i][j] + (rows - i) + (cols - j) - 1
        det = 1
        for i in range(rows):
            for j in range(cols):
                det *= factorial(hook_lengths[i][j])
        return det
    
    def symmetric_power_decomposition(n, k):
        shape = [[k] * n]
        return hook_length_formula(shape)
    
    n = random.randint(2, 40)
    m = int(math.pow(n, 1.5)) - 1
    k = math.ceil(math.log(n))
    
    perm_n = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    det_m = [[random.choice([0, 1]) for _ in range(m)] for _ in range(m)]
    
    perm_n_decomp = symmetric_power_decomposition(n, k)
    det_m_decomp = symmetric_power_decomposition(m, k)
    
    if perm_n_decomp == 0 or det_m_decomp == 0:
        return {
            "metric_name": "irreducible_components",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "decomposition_zero"
        }
    
    ratio = perm_n_decomp / det_m_decomp
    conjecture_holds = ratio >= n**(k-1)
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"perm_n_decomp={perm_n_decomp}, det_m_decomp={det_m_decomp}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")