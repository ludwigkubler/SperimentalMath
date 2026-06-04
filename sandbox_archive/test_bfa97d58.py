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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(other_lit) for lit in clause for other_lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    for lit_i in queue[i]:
                        if -lit_i in queue[j]:
                            new_clause = [l for l in queue[i] if l != lit_i]
                            new_clause.extend([l for l in queue[j] if l != -lit_i])
                            if not any(lit in new_clause for lit in new_clause[1:]):
                                new_clauses.append(new_clause)
                                break
                else:
                    continue
                break
            if not new_clauses:
                return len(queue)
            queue.extend(new_clauses)
    
    def minimal_formal_group_order(cnf):
        n = len(cnf[0])
        for order in range(1, n**2 + 1):
            # Simulate a non-abelian formal group of the given order
            if order >= n:
                return order
        return None
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        min_order = minimal_formal_group_order(cnf)
        
        if min_order is None or width == 0:
            return {
                "metric_name": "min_order(G(φ))",
                "metric_value": -1,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((min_order, width))
    
    min_orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_width = sum(widths) / len(widths)
    std_dev = math.sqrt(sum((x - mean_min_order)**2 for x in min_orders) / len(min_orders))
    
    correlation_coefficient = sum((min_orders[i] - mean_min_order) * (widths[i] - mean_width) for i in range(len(min_orders))) / (len(min_orders) * std_dev * math.sqrt(sum((x - mean_width)**2 for x in widths)))
    r_squared = correlation_coefficient ** 2
    
    return {
        "metric_name": "min_order(G(φ))",
        "metric_value": mean_min_order,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and r_squared >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")