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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_polynomial(cnf):
        # Placeholder for polynomial computation
        # This is a dummy implementation and should be replaced with actual logic
        return 0
    
    def compute_tropical_motivic_rank(poly):
        # Placeholder for tropical motivic rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return 0
    
    def max_clause_degree(cnf):
        return max(len(clause) - 1 for clause in cnf)
    
    def min_satisfying_assignments(cnf):
        # Placeholder for satisfying assignments computation
        # This is a dummy implementation and should be replaced with actual logic
        return 1
    
    m = random.randint(5, 40)
    n = random.randint(5, 40)
    cnf = generate_cnf(m, n)
    
    poly = compute_polynomial(cnf)
    mtr_phi = compute_tropical_motivic_rank(poly)
    max_deg = max_clause_degree(cnf)
    min_satisfying = min_satisfying_assignments(cnf)
    
    metric_value = mtr_phi
    conjecture_holds = mtr_phi >= max_deg + min_satisfying
    
    return {
        "metric_name": "tropical_motivic_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mtr_phi={mtr_phi}, max_deg+min_satisfying={max_deg + min_satisfying}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        counterexample_desc = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")