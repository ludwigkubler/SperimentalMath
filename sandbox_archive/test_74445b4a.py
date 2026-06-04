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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def polynomial_from_cnf(cnf):
        n = len(cnf[0])
        poly = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    poly[var][var] += 1
                else:
                    poly[var][var] -= 1
        return poly
    
    def minimal_order_of_invariants(poly):
        n = len(poly)
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                if poly[i][j] != 0:
                    order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poly = polynomial_from_cnf(cnf)
        order = minimal_order_of_invariants(poly)
        
        if order > n * (n - 1) // 2:
            return {
                "metric_name": "minimal_order_of_invariants",
                "metric_value": order,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"order > {n * (n - 1) // 2}"
            }
        
        results.append({
            "metric_name": "minimal_order_of_invariants",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(order - n * (n - 1) // 2) <= 3
        })
    
    return results[0]

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order > {n * (n - 1) // 2}\" first_failing_seed={first_failing_seed}")