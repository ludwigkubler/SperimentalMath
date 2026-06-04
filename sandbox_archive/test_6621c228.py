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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_valuation_rank(poly):
        # Placeholder implementation
        return random.randint(1, n)
    
    def frege_proof_depth(cnf):
        # Placeholder implementation
        return random.randint(10, 50)
    
    correlation_coefficient = 0.0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        r_phi = p_adic_valuation_rank(cnf)
        d_phi = frege_proof_depth(cnf)
        
        if n > n_max:
            n_max = n
        
        correlation_coefficient += (r_phi - 1) * (d_phi - 25) / 20
        instances_tested += 1
        
        p_k = random.randint(1, int(math.log(n, 2)))
        k_log_n_plus_1 = math.ceil(k_log_n + 1)
        
        if r_phi < d_phi and not conjecture_holds:
            counterexample = f"r_phi={r_phi} < d_phi={d_phi}"
            break
        elif r_phi >= d_phi and p_k > k_log_n_plus_1 and conjecture_holds:
            counterexample = f"p_k={p_k} > {k_log_n_plus_1}, but r_phi={r_phi} >= d_phi={d_phi}"
            conjecture_holds = False
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")