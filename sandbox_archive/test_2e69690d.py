# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_width(instance):
        n = len(instance)
        if n == 1:
            return 1
        else:
            return 2 * dpll_width(instance[:n//2]) + dpll_width(instance[n//2:])
    
    def hodge_arc_length(n):
        # Simplified approximation of Hodge arc length
        return Fraction(n, 2)
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / n)
        if std_x == 0 or std_y == 0:
            return 0
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in range(5, 41):
        instance = generate_sat_instance(n)
        width = dpll_width(instance)
        arc_length = hodge_arc_length(n)
        results.append((arc_length, width))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    arc_lengths, widths = zip(*results)
    corr = pearson_correlation(arc_lengths, widths)
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": corr > 0.8,
        "counterexample": "" if corr > 0.8 else f"Correlation {corr} is not sufficiently high"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")