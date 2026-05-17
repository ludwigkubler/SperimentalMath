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

def eulerian_number(n, k):
    if n == 1 or k == 0 or k == n - 1:
        return 1
    return ((n - k) * eulerian_number(n - 1, k - 1) + (k + 1) * eulerian_number(n - 1, k))

def compute_entropy(n):
    coefficients = [eulerian_number(n, k) for k in range(n)]
    total = sum(coefficients)
    probabilities = [coeff / total for coeff in coefficients]
    entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [4, 5, 6, 7, 8]
    results = []
    
    for n in n_values:
        entropy = compute_entropy(n)
        if entropy < 1.0:
            return {
                "metric_name": "rho(perm_n)",
                "metric_value": entropy,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rho(perm_n)={entropy}"
            }
        results.append(entropy)
    
    return {
        "metric_name": "rho(perm_n)",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1.0) / len(results)
    
    if all(r >= 1.0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 1.0)
        print(f"RESULT: FALSIFIED counterexample='n=4, rho(perm_n)<1' first_failing_seed={first_failing_seed}")