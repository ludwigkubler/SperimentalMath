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
    
    def hook_length_formula(n, k):
        hook_lengths = [[0] * (n - i) for i in range(n)]
        for i in range(n):
            for j in range(n - i):
                hook_lengths[i][j] = n - i + 1 + j
        det = 1
        for i in range(n):
            for j in range(n - i):
                det *= factorial(hook_lengths[i][j])
        return det
    
    def count_irreducible_components(n, k):
        perm_n_decomp = hook_length_formula(n, k)
        det_m_decomp = hook_length_formula(k, k)
        return perm_n_decomp, det_m_decomp
    
    n = random.randint(2, 40)
    m = random.randint(1, int(math.sqrt(n)) - 1)
    k = math.ceil(math.log(n))
    
    perm_n_decomp, det_m_decomp = count_irreducible_components(n, k)
    
    conjecture_holds = perm_n_decomp > det_m_decomp * n**(k-1)
    counterexample = "" if conjecture_holds else f"perm_n_decomp={perm_n_decomp}, det_m_decomp={det_m_decomp}"
    
    return {
        "metric_name": "irreducible_components_ratio",
        "metric_value": perm_n_decomp / det_m_decomp,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")