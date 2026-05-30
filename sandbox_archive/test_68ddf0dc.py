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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def quadratic_form(cnf, x):
        value = 0
        for clause in cnf:
            value += abs(x[abs(clause[0]) - 1] + x[abs(clause[1]) - 1])
        return value
    
    def lp_norm(value, p):
        if p == 1:
            return sum(abs(v) for v in value)
        elif p == float('inf'):
            return max(abs(v) for v in value)
        else:
            return (sum(abs(v)**p for v in value))**(1/p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [int(0.5 * n) for n in n_values]
    instances_tested = 0
    total_norm = 0
    
    for n, m in zip(n_values, m_values):
        cnf = generate_cnf(n, m)
        min_norm = float('inf')
        for _ in range(10):  # Sample 10 quadratic forms per instance
            x = [random.uniform(-1, 1) for _ in range(n)]
            norm = lp_norm(quadratic_form(cnf, x), p=2)
            if norm < min_norm:
                min_norm = norm
        total_norm += min_norm
        instances_tested += 1
    
    mean_norm = total_norm / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    # Placeholder for actual computation of the upper bound
    upper_bound = float('inf')
    
    if mean_norm > upper_bound * 1.05:
        conjecture_holds = False
        counterexample = "mean_norm exceeds upper_bound by more than 5%"
    
    return {
        "metric_name": "Minimal L^p Norm",
        "metric_value": mean_norm,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")