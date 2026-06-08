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
        for _ in range(10):  # Generate 10 random clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        depth = 0
        for clause in cnf:
            depth += len(clause)
        return depth
    
    def p_adic_order(poly):
        order = 0
        while poly % p == 0 and poly != 0:
            poly //= p
            order += 1
        return order
    
    def polynomial_from_cnf(cnf, p):
        n = max(abs(lit) for clause in cnf for lit in clause)
        poly = [0] * (n + 1)
        for clause in cnf:
            product = 1
            for lit in clause:
                if lit > 0:
                    product *= (x**lit)
                else:
                    product *= ((-x)**(-lit))
            poly += product
        return poly
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        d = frege_proof_depth(cnf)
        p = random.choice([3, 5, 7, 11])  # Choose a random odd prime
        poly = polynomial_from_cnf(cnf, p)
        order = p_adic_order(poly)
        
        results.append({
            "n": n,
            "d": d,
            "order": order
        })
    
    min_order = min(result["order"] for result in results)
    avg_d = sum(result["d"] for result in results) / len(results)
    
    if min_order >= 0.1 * avg_d:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "min_order < 0.1 * avg_d"
    
    return {
        "metric_name": "p-adic order",
        "metric_value": min_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")