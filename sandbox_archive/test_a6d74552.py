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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if any(x != 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        n = len(cnf[0])
        resolvents = set()
        queue = cnf.copy()
        
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                for i, x in enumerate(clause1):
                    if x == -clause2[i]:
                        resolvent = [x for x in clause1 + clause2 if x != 0 and x != -x]
                        resolvent.sort()
                        if tuple(resolvent) not in resolvents:
                            resolvents.add(tuple(resolvent))
                            queue.append(resolvent)
            if len(queue) > n * (n + 1) / 2:
                return float('inf')
        return max(len(r) for r in resolvents)
    
    def minimal_quadratic_residues_order(n):
        residues = set()
        for i in range(1, n**2 + 1):
            if pow(i, (n - 1) // 2, n) == 1:
                residues.add(i)
        return len(residues)
    
    orders = []
    widths = []
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            width = resolution_width(cnf)
            if width == float('inf'):
                continue
            order = minimal_quadratic_residues_order(n)
            orders.append(order)
            widths.append(width)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not orders or not widths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = 0
    numerator = sum((o - mean_order) * (w - mean_width) for o, w in zip(orders, widths))
    denominator = math.sqrt(sum((o - mean_order)**2 for o in orders)) * math.sqrt(sum((w - mean_width)**2 for w in widths))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")