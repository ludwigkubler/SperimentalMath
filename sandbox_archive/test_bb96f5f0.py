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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def frege_proof_depth(cnf):
        depth = 0
        for clause in cnf:
            if len(clause) == 1:
                depth += 1
            else:
                depth += 2
        return depth

    def p_adic_order(poly, p):
        order = 0
        while poly % p == 0:
            poly //= p
            order += 1
        return order

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    d_phi = frege_proof_depth(cnf)
    
    # Construct polynomial representation using p-adic field
    p = random.choice([3, 5, 7, 11, 13])  # Choose an odd prime
    poly = 0
    for clause in cnf:
        term = 1
        for var in clause:
            if var > 0:
                term *= (var + n)
            else:
                term *= (-var)
        poly += term

    ord_p_poly = p_adic_order(poly, p)

    return {
        "metric_name": "p-adic Order / Frege Proof Depth",
        "metric_value": ord_p_poly / d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_p_poly >= 0.5 * d_phi,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        int(random.choice([2**i + 3 for i in range(5, 10)])) for _ in range(30)
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")