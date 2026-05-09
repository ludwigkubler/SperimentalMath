# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.randint(1, n) for _ in range(3))
        cnf.append(clause)
    return cnf

def polynomial_encoding(cnf):
    n = max(max(clause) for clause in cnf)
    variables = [0] * n
    poly = 1
    p = 2  # Using p-adic valuation over Q_2 (binary)
    
    for clause in cnf:
        term = 1
        for v in clause:
            if random.choice([True, False]):
                term *= variables[v - 1]
            else:
                term *= (1 - variables[v - 1])
        poly += term
    
    return p, poly

def p_adic_valuation(poly, p):
    valuation = 0
    while poly % p == 0 and poly != 0:
        poly //= p
        valuation += 1
    return valuation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, 2 * n)
        p, poly = polynomial_encoding(cnf)
        
        valuations = [p_adic_valuation(coeff, p) for coeff in poly.coefficients()]
        distinct_valuations = len(set(valuations))
        
        instances_tested = len(valuations)
        conjecture_holds = False
        counterexample = ""
        
        if n <= 40:
            expected_valuation_rank = math.log(n, 2)
            expected_circuit_size = n**3 * 10**6  # Simplified upper bound for ACC^0 circuit size
            
            if abs(distinct_valuations - expected_valuation_rank) < 1 and poly.size() <= expected_circuit_size:
                conjecture_holds = True
            else:
                counterexample = f"n={n}, distinct_valuations={distinct_valuations}, expected_valuation_rank={expected_valuation_rank}, poly_size={poly.size()}, expected_circuit_size={expected_circuit_size}"
        
        results.append({
            "metric_name": "valuation_rank",
            "metric_value": distinct_valuations,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    total_valuation_rank = sum(sum(trial["results"][0]["metric_value"] for trial in results) for results in all_results)
    num_trials = len(all_results)
    avg_valuation_rank = total_valuation_rank / num_trials
    
    support_fraction = sum(any(trial["results"][0]["conjecture_holds"] for trial in results) for results in all_results) / num_trials
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_valuation_rank:.2f} std=... support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, results in enumerate(all_results, start=1) if not any(trial["results"][0]["conjecture_holds"] for trial in results))
        print(f"RESULT: FALSIFIED counterexample=\"valuation_rank_mismatch\" first_failing_seed={first_failing_seed}")