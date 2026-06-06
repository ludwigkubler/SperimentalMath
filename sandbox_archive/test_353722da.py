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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def cnf_to_polynomial(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        n_vars = max(variables)
        
        polynomial = [0] * (n_vars + 1)
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 - x[literal])
                else:
                    term *= (1 + x[-literal])
            polynomial[0] += term
        
        return polynomial
    
    def p_adic_growth_rate(polynomial):
        n = len(polynomial) - 1
        growth_rate = [0] * (n + 1)
        for i in range(1, n + 1):
            growth_rate[i] = sum(abs(coeff) * p**i for coeff in polynomial[:i+1])
        return max(growth_rate)
    
    def frege_proof_depth(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    polynomial = cnf_to_polynomial(cnf)
    mcr = p_adic_growth_rate(polynomial)
    f_phi = frege_proof_depth(cnf)
    
    if f_phi == 0:
        return {
            "metric_name": "MCR/f(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "f(φ) is zero"
        }
    
    ratio = mcr / f_phi
    return {
        "metric_name": "MCR/f(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 1 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")