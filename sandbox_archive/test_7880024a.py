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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def tropicalized_barycentric_coordinates(f):
        n = len(f)
        if n == 1:
            return [f[0]]
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        left_coords = tropicalized_barycentric_coordinates(left)
        right_coords = tropicalized_barycentric_coordinates(right)
        coords = []
        for i in range(len(left_coords)):
            coords.append(max(left_coords[i], right_coords[i]))
        return coords
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        var_x = sum((xi - mean_x)**2 for xi in x) / n
        var_y = sum((yi - mean_y)**2 for yi in y) / n
        if var_x == 0 or var_y == 0:
            return 0
        return cov_xy / math.sqrt(var_x * var_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        rank = len(tropicalized_barycentric_coordinates(f))
        width = xor_and_tree_width(f)
        ranks.append(rank)
        widths.append(width)
    
    correlation_coefficient = pearson_correlation_coefficient(ranks, widths)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": "" if correlation_coefficient > 0.9 else f"Correlation coefficient {correlation_coefficient} is not significantly higher than expected by chance"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")