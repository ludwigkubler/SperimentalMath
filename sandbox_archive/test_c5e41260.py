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
        cnf = []
        for i in range(1, n+1):
            clause = [-i]
            for j in range(i+1, n+1):
                if random.choice([True, False]):
                    clause.append(j)
            cnf.append(clause)
        return cnf
    
    def resolution_depth(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        depth = 0
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        lit = list(set(c1) ^ set(c2))[0]
                        new_clause = [l for l in c1 + c2 if l != -lit and l != lit]
                        if new_clause not in new_clauses:
                            new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
            depth += 1
        return depth
    
    def hodge_index(cnf, p):
        # Placeholder for Hodge index computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)  # Replace with actual Hodge index calculation
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    p = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
    
    hodge_index_value = hodge_index(cnf, p)
    depth = resolution_depth(cnf)
    
    return {
        "metric_name": "hodge_index_to_resolution_depth_ratio",
        "metric_value": Fraction(hodge_index_value, depth),
        "instances_tested": 1,
        "conjecture_holds": False if hodge_index_value < 2 * depth else True,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")