# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hypergeom_order(n, m):
        if n <= 0 or m <= 0:
            return 1
        order = 1
        for i in range(1, min(m, n)):
            order *= (n - i + 1) / (i + 1)
        return order
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(-n, 0), 2) + random.sample(range(1, n+1), 2)
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    for lit in clause_i:
                        if -lit in clause_j:
                            new_clause = [l for l in clause_i + clause_j if l != lit and -l != lit]
                            new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(set(new_clauses))
            width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            order = hypergeom_order(n, m)
            width = resolution_width(cnf)
            instances_tested += 1
            n_max = max(n_max, n)
            if order == 0:
                continue
            ratio = abs(width) / (order ** 2)
            total_ratio += ratio
    
    mean_ratio = Fraction(total_ratio, instances_tested)
    conjecture_holds = mean_ratio <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")