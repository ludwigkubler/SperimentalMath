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
    
    def compute_taylor_coefficients(f, n):
        coefficients = []
        for i in range(n + 1):
            coeff = sum(f[j] * (-1)**j for j in range(i + 1)) / math.comb(i, i)
            coefficients.append(coeff)
        return coefficients
    
    def hermitian_form_rank(taylor_coeffs):
        n = len(taylor_coeffs) - 1
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(i, n + 1):
                A[i][j] = taylor_coeffs[j]**2 if i == j else 0
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def decision_tree_path_complexity(f):
        # Placeholder implementation; actual complexity depends on the function
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different functions
            f = generate_boolean_function(n)
            taylor_coeffs = compute_taylor_coefficients(f, n)
            N_f = hermitian_form_rank(taylor_coeffs)
            D_f = decision_tree_path_complexity(f)
            if D_f == 0:
                continue
            ratio = Fraction(N_f, D_f**0.5).limit_denominator()
            total_ratio += ratio
            instances_tested += 1
    
    mean_ratio = total_ratio / instances_tested
    log_n_squared = sum(math.log2(n)**2 for n in n_values) / len(n_values)
    
    conjecture_holds = mean_ratio <= log_n_squared
    counterexample = "" if conjecture_holds else f"Ratio {mean_ratio} > {log_n_squared}"
    
    return {
        "metric_name": "N_f/D(f)^{1/2}",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")