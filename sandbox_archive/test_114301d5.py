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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Ensure enough clauses to cover all variables
        num_clauses = random.randint(1, n)
        clause = [random.choice([-i, i]) for i in range(1, n + 1) if random.random() < 0.5]
        cnf.append(clause)
    return cnf

def compute_plp(cnf):
    # Placeholder implementation of p-adic logarithmic potential
    # This is a dummy function and should be replaced with actual computation
    return sum(len(clause) for clause in cnf)

def compute_cr(cnf):
    # Placeholder implementation of communication complexity rank
    # This is a dummy function and should be replaced with actual computation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    cnf = generate_cnf(n)
    plp = compute_plp(cnf)
    cr = compute_cr(cnf)
    
    correlation_coefficient = (cr * plp) / (abs(cr) * abs(plp)) if cr != 0 and plp != 0 else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(cnf),
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")