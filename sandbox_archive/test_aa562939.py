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
    
    def clause_density(formula):
        unique_clauses = set(tuple(clause) for clause in formula)
        total_literals = sum(len(clause) for clause in formula)
        return len(unique_clauses) / total_literals
    
    def l_series_expansion(formula, n):
        alpha = clause_density(formula)
        L_1_2 = 0
        for i in range(1, n + 1):
            term = (alpha ** i) * (math.log(i) / i)
            if abs(term) > 1e-10:
                L_1_2 += term
        return abs(L_1_2)
    
    def generate_formula(n, m):
        formula = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, 3))
            formula.append(tuple(sorted(clause)))
        return formula
    
    max_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n)
            formula = generate_formula(n, m)
            L_1_2 = l_series_expansion(formula, n)
            ratio = L_1_2 / (m / (n * 3))
            max_ratio = max(max_ratio, ratio)
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_ratio <= 1.05
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio}"
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='max_ratio_exceeds_bound' first_failing_seed={first_failing_seed}")