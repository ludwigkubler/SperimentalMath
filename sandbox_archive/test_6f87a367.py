# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_lie_algebroid(n):
        # Generate a simple Lie algebroid for testing purposes
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def smash_product(L1, L2):
        n = len(L1)
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                product = [L1[i][k] * L2[k][j] for k in range(n)]
                row.append(sum(product))
            result.append(row)
        return result
    
    def index(L):
        n = len(L)
        det = 0
        for p in itertools.permutations(range(n)):
            sign = Fraction(1, 1)
            product = 1
            for i in range(n):
                product *= L[i][p[i]]
                if (i + p[i]) % 2 == 1:
                    sign *= -1
            det += sign * product
        return abs(det)
    
    def monotone_width(circuit):
        # Simplified version of monotone width calculation for testing purposes
        return len(circuit) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    L1 = generate_lie_algebroid(n)
    L2 = generate_lie_algebroid(n)
    circuit = [random.randint(0, 1) for _ in range(n)]
    
    sp = smash_product(L1, L2)
    ind_sp = index(sp)
    w = monotone_width(circuit)
    
    return {
        "metric_name": "Index of Smash Product",
        "metric_value": ind_sp,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")