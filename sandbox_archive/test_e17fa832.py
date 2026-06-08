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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank / (2 * n * (n - 1))
    
    def eta_invariant(f):
        n = len(f)
        count = [0] * (n + 1)
        for i in range(2**n):
            count[sum(f[j] << j for j in range(n))] += 1
        return sum(count[i] ** 2 for i in range(n + 1)) / (2 ** n)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov / (std_x * std_y)
    
    def p_value(r, n):
        if abs(r) >= 1:
            return 0
        t = r * (n - 2) ** 0.5 / ((1 - r**2) ** 0.5)
        df = n - 2
        return 2 * (1 - Fraction(1, 2) * beta(df / 2, 0.5))
    
    def beta(a, b):
        if a <= 0 or b <= 0:
            return 0
        return gamma(a + b) / (gamma(a) * gamma(b))
    
    def gamma(x):
        if x == 1:
            return 1
        elif x < 1:
            return gamma(x + 1) / x
        else:
            return (x - 0.5) * math.log(x) - x + 0.9189385332046727
    
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    rank_variance_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        eta_values.append(eta_invariant(f))
        rank_variance_values.append(communication_complexity_rank_variance(f))
    
    correlation = pearson_correlation(eta_values, rank_variance_values)
    p_val = p_value(correlation, len(eta_values))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and p_val <= 0.05,
        "counterexample": "" if correlation >= 0.8 and p_val <= 0.05 else "Pearson correlation < 0.8 or p-value > 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")