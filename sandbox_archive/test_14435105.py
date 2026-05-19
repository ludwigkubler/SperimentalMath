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

def hook_length_formula(n, partition):
    def hook_length(y, x):
        return (n - y) * (n - x + 1) // (y - x)
    
    total = 1
    for i in range(len(partition)):
        for j in range(i + 1):
            total *= hook_length(partition[i] - j, j)
    for i in range(1, len(partition)):
        for j in range(len(partition) - i):
            total *= hook_length(partition[j], partition[j + i])
    
    return Fraction(total)

def schur_polynomial(n, partition):
    def minor(m, n, k):
        if m == 0 or n == 0:
            return 1
        elif m < n:
            return 0
        else:
            return sum((-1)**(k - j) * minor(m - i, n - 1, j) for i in range(n + 1))
    
    def schur_elementary(a, b):
        if a == b:
            return 1
        elif a < b:
            return 0
        else:
            return sum((-1)**(a - b - k) * minor(a - b - k, k, b) for k in range(b + 1))
    
    det = 1
    for i in range(len(partition)):
        det *= schur_elementary(n - partition[i], i)
    return det

def multiplicity(n, partition):
    dim = hook_length_formula(n, partition)
    schur = schur_polynomial(n, partition)
    return Fraction(dim * schur).numerator // dim.denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sym_multiplicity = multiplicity(n, (n-1, 1))
        antisym_multiplicity = multiplicity(n, (n-1, 1))
        
        if sym_multiplicity <= antisym_multiplicity:
            return {
                "metric_name": "Multiplicity Gap",
                "metric_value": antisym_multiplicity - sym_multiplicity,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, symmetric multiplicity={sym_multiplicity}, antisymmetric multiplicity={antisym_multiplicity}"
            }
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": 0,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity gap does not hold\" first_failing_seed={first_failing_seed}")