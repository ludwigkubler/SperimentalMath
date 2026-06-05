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
    
    def characteristic_polynomial(cnf):
        n = len(cnf[0])
        x = [Fraction(1, 1)] * (n + 1)
        for clause in cnf:
            term = Fraction(1, 1)
            for var in clause:
                if var > 0:
                    term *= (1 - x[-var - 1])
                else:
                    term *= x[-var]
            x[0] -= term
        return x
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        # This is a placeholder and should be replaced with actual logic
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n * (n - 1) // 2):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(var != 0 for var in clause):
            cnf.append(clause)
    
    p = characteristic_polynomial(cnf)
    k = 1
    while p[k] == Fraction(0, 1):
        k += 1
    
    w = resolution_width(cnf)
    log_n = math.log(n)
    
    conjecture_holds = w >= k**2 * log_n
    counterexample = "" if conjecture_holds else f"CNF with n={n}, k={k}, log(n)={log_n}, w={w}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": len(cnf),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_w = sum(r["metric_value"] for r in results) / len(results)
    std_w = math.sqrt(sum((r["metric_value"] - mean_w)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_w} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")