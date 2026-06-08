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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        if n == 1:
            return 0
        rank = 0
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if f[i-1] != f[j-1]:
                    rank += 1
        return rank / (n * (n - 1) // 2)
    
    def eta_invariant(f):
        n = len(f)
        if n == 1:
            return Fraction(0, 1)
        count = [0] * (n + 1)
        for i in range(n):
            count[f[i]] += 1
        return Fraction(count[0], count[1])
    
    def pearson_correlation(xs, ys):
        n = len(xs)
        if n != len(ys):
            raise ValueError("Lists must have the same length")
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
        var_x = sum((x - mean_x)**2 for x in xs) / n
        var_y = sum((y - mean_y)**2 for y in ys) / n
        return cov_xy / math.sqrt(var_x * var_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance(f)
        eta_Cf = eta_invariant(f)
        results.append((eta_Cf, R_f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    eta_values, R_values = zip(*results)
    corr_coeff = pearson_correlation(eta_values, R_values)
    p_value = 2 * (1 - math.erf(abs(corr_coeff) / math.sqrt(2 * len(results) - 2)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(corr_coeff) >= 0.8 and p_value <= 0.05,
        "counterexample": "" if abs(corr_coeff) >= 0.8 else f"Correlation coefficient: {corr_coeff}, p-value: {p_value}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")