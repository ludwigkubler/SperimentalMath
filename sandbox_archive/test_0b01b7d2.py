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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(lit not in clause and -lit not in clause for lit in cnf):
                cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        seen = set()
        queue = list(cnf)
        while queue:
            clause = queue.pop(0)
            for literal in clause:
                if literal > 0:
                    opposite = -literal
                else:
                    opposite = -literal
                if opposite in seen:
                    return len(queue) + 1
                seen.add(literal)
                for other_clause in cnf:
                    if literal in other_clause and -opposite in other_clause:
                        new_clause = [l for l in other_clause if l != literal and l != -opposite]
                        if new_clause not in queue:
                            queue.append(new_clause)
        return float('inf')
    
    def minimal_order(cnf):
        n = len(cnf[0])
        coefficients = [Fraction(1, 2**i) for i in range(n)]
        series = sum(coeff * x**(n-i-1) for i, coeff in enumerate(coefficients))
        return series
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        order = minimal_order(cnf)
        results.append((width, order))
    
    widths = [w for w, _ in results]
    orders = [o for _, o in results]
    
    if len(widths) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_width = sum(widths) / len(widths)
    mean_order = sum(orders) / len(orders)
    correlation_coefficient = sum((w - mean_width) * (o - mean_order) for w, o in results) / (len(results) * math.sqrt(sum((w - mean_width)**2 for w in widths)) * math.sqrt(sum((o - mean_order)**2 for o in orders)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")