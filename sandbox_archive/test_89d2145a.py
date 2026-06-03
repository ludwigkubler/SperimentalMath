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
    
    def generate_category(n):
        if n == 1:
            return {0: set()}
        objects = list(range(n))
        morphisms = {}
        for i in range(n):
            for j in range(i+1, n):
                morphisms[(i, j)] = {j}
        return {0: set(), **morphisms}
    
    def min_order(category):
        if not category:
            return 0
        objects = list(category.keys())
        min_ranks = [len(category[obj]) for obj in objects]
        return max(min_ranks)
    
    def circuit_monotone_width(category):
        n = len(category[0])
        cnf = []
        for i in range(n):
            clause = set()
            for j in range(i+1, n):
                if (i, j) in category and j in category[i]:
                    clause.add(j)
            cnf.append(clause)
        return len(cnf)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    def mean_absolute_difference(x, y):
        return sum(abs(xi - yi) for xi, yi in zip(x, y)) / len(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    m_values = []
    
    for n in n_values:
        category = generate_category(n)
        min_order_val = min_order(category)
        m_val = circuit_monotone_width(category)
        min_orders.append(min_order_val)
        m_values.append(m_val)
    
    correlation = correlation_coefficient(min_orders, m_values)
    mean_diff = mean_absolute_difference(min_orders, m_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 2,
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 2 else f"correlation={correlation}, mean_diff={mean_diff}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation or mean_diff criteria not met\" first_failing_seed={first_failing_seed}")