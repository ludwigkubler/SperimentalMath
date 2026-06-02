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
    
    def generate_polynomial(d):
        coeffs = [random.randint(1, 10) for _ in range(d + 1)]
        return coeffs
    
    def evaluate_polynomial(coeffs, x):
        result = 0
        for i, coeff in enumerate(coeffs):
            result += coeff * (x ** i)
        return result
    
    def find_roots(coeffs):
        n = len(coeffs) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-coeffs[0] / coeffs[1]]
        
        roots = []
        for k in range(1, n + 1):
            for i in range(n - k + 1):
                a_k = sum(coeffs[j] * math.comb(k, j) * (-1) ** (k - j) for j in range(i, i + k))
                if a_k == 0:
                    continue
                b_k = sum(coeffs[j] * math.comb(n - k, j - i) * (-1) ** (n - k - j) for j in range(i + k, n + 1))
                root = Fraction(b_k, a_k)
                if root not in roots:
                    roots.append(root)
        return roots
    
    def monotone_width(coeffs):
        n = len(coeffs) - 1
        width = 0
        for i in range(1, n + 1):
            max_val = -float('inf')
            min_val = float('inf')
            for j in range(n - i + 1):
                val = evaluate_polynomial(coeffs, j)
                if val > max_val:
                    max_val = val
                if val < min_val:
                    min_val = val
            width += max_val - min_val
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    d_values = [5, 10, 15, 20, 30, 40]
    m_min_dist_sum = 0
    width_sum = 0
    instances_tested = 0
    
    for d in d_values:
        for _ in range(5):
            coeffs = generate_polynomial(d)
            roots = find_roots(coeffs)
            if len(roots) > 1:
                m_min_dist = min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i + 1, len(roots)))
                width = monotone_width(coeffs)
                m_min_dist_sum += m_min_dist
                width_sum += width
                instances_tested += 1
    
    mean_m_min_dist = m_min_dist_sum / instances_tested
    mean_width = width_sum / instances_tested
    correlation = pearson_correlation([m_min_dist_sum], [width_sum])
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation does not meet threshold\" first_failing_seed={first_failing_seed}")