# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def xor_and_tree_width(cnf):
        # Simplified XOR-AND tree width calculation
        return len(cnf)
    
    def tropicalize_group(order):
        # Placeholder for group tropicalization logic
        return order
    
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            width = xor_and_tree_width(cnf)
            order = tropicalize_group(width)
            total_order += order
            total_width += width
            instances_tested += 1
    
    mean_order = Fraction(total_order, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    if instances_tested < 30:
        return {
            "metric_name": "Proportionality Slope",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        if sum_xx == 0:
            return None, None
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = mean_y - slope * mean_x
        return slope, intercept
    
    slope, _ = linear_regression([mean_width] * instances_tested, [mean_order] * instances_tested)
    
    return {
        "metric_name": "Proportionality Slope",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "conjecture_holds": slope is not None and slope >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample='Slope less than 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient evidence to support or refute the conjecture")