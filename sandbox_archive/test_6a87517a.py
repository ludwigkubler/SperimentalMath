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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return float('inf')
        
        width = 0
        for i in range(n):
            count = sum(1 for x in f if (x >> i) & 1)
            width = max(width, count, n - count)
        return width
    
    def quotient_algebra(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return float('inf')
        
        algebra = set()
        for x in range(2**n):
            for y in range(2**n):
                if (x & y) == 0 and f[x] == f[y]:
                    algebra.add((x, y))
        return len(algebra)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x != 0 and std_y != 0 else float('nan')
    
    def is_linearly_correlated(r, threshold=0.8):
        return abs(r) >= threshold
    
    def is_within_bound(rank, width):
        return rank <= 5 * width
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        width = monotone_width(f)
        rank = quotient_algebra(f)
        
        if width == float('inf') or rank == float('inf'):
            continue
        
        ranks.append(rank)
        widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = pearson_correlation(ranks, widths)
    all_within_bound = all(is_within_bound(rank, width) for rank, width in zip(ranks, widths))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": is_linearly_correlated(correlation) and all_within_bound,
        "counterexample": "" if is_linearly_correlated(correlation) and all_within_bound else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")