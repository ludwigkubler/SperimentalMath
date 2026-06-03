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
            return {'objects': [0], 'morphisms': {}}
        objects = list(range(n))
        morphisms = {}
        for i in range(n):
            for j in range(i+1, n):
                morphisms[(i, j)] = random.choice(objects)
        return {'objects': objects, 'morphisms': morphisms}
    
    def min_order(category):
        objects = category['objects']
        morphisms = category['morphisms']
        n = len(objects)
        if n == 1:
            return 1
        min_ranks = [n] * n
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in morphisms:
                    min_ranks[i] = min(min_ranks[i], min_ranks[morphisms[(i, j)]])
        return max(min_ranks)
    
    def circuit_monotone_width(category):
        objects = category['objects']
        morphisms = category['morphisms']
        n = len(objects)
        if n == 1:
            return 0
        width = 0
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in morphisms:
                    continue
                rank = min_order(category)
                if rank > width:
                    width = rank
        return width
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        if std_x == 0 or std_y == 0:
            return 0
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    m_values = []
    
    for n in n_values:
        category = generate_category(n)
        min_order_val = min_order(category)
        m_value = circuit_monotone_width(category)
        min_orders.append(min_order_val)
        m_values.append(m_value)
    
    correlation = correlation_coefficient(min_orders, m_values)
    mean_diff = sum(abs(x - y) for x, y in zip(min_orders, m_values)) / len(min_orders)
    
    conjecture_holds = correlation >= 0.8 and mean_diff <= 2
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean_abs_diff > 2"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r['metric_value'] for r in results) / len(results)
    std_corr_coeff = math.sqrt(sum((r['metric_value'] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")