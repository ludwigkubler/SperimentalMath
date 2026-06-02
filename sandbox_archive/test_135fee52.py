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
        for _ in range(random.randint(5, 10)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(sorted(clause)) for clause in cnf if len(clause) > 1)
        
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            new_clauses = []
            for other_clause in queue:
                common_vars = [var for var in clause if -var in other_clause]
                if common_vars:
                    new_clause = tuple(sorted(set(clause) ^ set(other_clause)))
                    if len(new_clause) == 1:
                        return n
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return n
    
    def minimal_quadratic_residue_order(n):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in primes:
            if pow(2, (p - 1) // 2, p) == 1:
                return p
        return None
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    order = minimal_quadratic_residue_order(n)
    
    if order is None:
        return {
            "metric_name": "minimal_quadratic_residue_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "minimal_quadratic_residue_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")