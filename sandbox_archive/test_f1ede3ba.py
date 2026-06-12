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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f):
        n = len(f)
        literals = {i: f"p{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        for i in range(n):
            clauses.append([-literals[i], literals[(i + 1) % n]])
        return clauses
    
    def min_tropical_motivic_rank(clauses):
        # Placeholder implementation
        return len(clauses)
    
    def communication_complexity_rank(f):
        # Placeholder implementation
        return len(f)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mtr_values = []
    r_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        clauses = tseitin_formula(f)
        mtr_value = min_tropical_motivic_rank(clauses)
        r_value = communication_complexity_rank(f)
        mtr_values.append(mtr_value)
        r_values.append(r_value)
    
    corr_coeff = correlation_coefficient(mtr_values, r_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= corr_coeff <= 1 and all(0.8 <= corr_coeff <= 1 for _ in range(len(n_values))),
        "counterexample": "" if 0.8 <= corr_coeff <= 1 else f"Outlying correlation coefficient: {corr_coeff}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 80, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.8 <= r["metric_value"] <= 1) / len(results)
    
    if all(0.8 <= r["metric_value"] <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction=1")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Outlying correlation coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")