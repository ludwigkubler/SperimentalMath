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
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n * 5)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        max_width = 0
        for clause in cnf:
            max_width = max(max_width, len(set(abs(x) for x in clause)))
        return max_width
    
    def minimal_order_of_quadratic_residues(n):
        residues = set()
        for i in range(1, n + 1):
            residues.add(i * i % n)
        return len(residues)
    
    orders = []
    widths = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_random_cnf(n)
        order = minimal_order_of_quadratic_residues(n)
        width = resolution_width(cnf)
        
        orders.append(order)
        widths.append(width)
        instances_tested += len(cnf)
        n_max = max(n_max, n)
    
    correlation_coefficient = 0
    if len(orders) > 1 and len(widths) > 1:
        mean_order = sum(orders) / len(orders)
        mean_width = sum(widths) / len(widths)
        numerator = sum((x - mean_order) * (y - mean_width) for x, y in zip(orders, widths))
        denominator = math.sqrt(sum((x - mean_order) ** 2 for x in orders)) * math.sqrt(sum((y - mean_width) ** 2 for y in widths))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.4f} < 0.7"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")