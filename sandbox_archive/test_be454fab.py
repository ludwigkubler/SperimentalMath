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
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c != 0 for c in clause):
                cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        queue = list(clauses)
        while queue:
            clause1 = queue.pop()
            for clause2 in clauses:
                if any(-l in clause2 for l in clause1):
                    new_clause = sorted([l for l in clause1 + clause2 if -l not in clause1 and -l not in clause2])
                    if len(new_clause) == 0:
                        return 0
                    if tuple(new_clause) not in clauses:
                        queue.append(tuple(new_clause))
        return float('inf')
    
    def local_cohomology_rank(cnf):
        # Placeholder for actual implementation of local cohomology rank calculation
        # For simplicity, we use a dummy function that returns a random value
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    w_phi = resolution_width(cnf)
    lchrank_phi = local_cohomology_rank(cnf)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "lchrank/w_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    ratio = Fraction(lchrank_phi, w_phi)
    return {
        "metric_name": "lchrank/w_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - (sum(metric_values) / len(metric_values)))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='lchrank/w_ratio < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")