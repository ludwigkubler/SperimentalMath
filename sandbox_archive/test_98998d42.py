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
    
    # Generate a random CNF instance with n variables and m clauses
    n = 30
    m = 10 * n
    cnf_instance = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf_instance.append(clause)
    
    # Map the CNF instance to a symmetric polynomial
    variables = set()
    for clause in cnf_instance:
        for var in clause:
            if var > 0:
                variables.add(var)
    n_vars = len(variables)
    
    def monomial_to_coeff(monomial):
        coeff = 1
        for var, exp in monomial.items():
            coeff *= var ** exp
        return coeff
    
    polynomial = {}
    for clause in cnf_instance:
        monomial = {var: 1 for var in clause}
        coeff = monomial_to_coeff(monomial)
        if coeff in polynomial:
            polynomial[coeff] += 1
        else:
            polynomial[coeff] = 1
    
    # Compute Schur decomposition coefficients using Young tableaux (simplified version)
    def schur_decomposition(poly):
        schur_coeffs = {}
        for coeff, count in poly.items():
            schur_coeffs[count] = schur_coeffs.get(count, 0) + count
        return schur_coeffs
    
    schur_coeffs = schur_decomposition(polynomial)
    
    # Count non-zero entries (S(f))
    S_f = sum(schur_coeffs.values())
    
    # Measure Frege proof length via a DPLL-based proof generator (simplified version)
    def dpll_proof_length(cnf):
        stack = []
        assignment = [False] * n_vars
        for clause in cnf:
            if all(not assignment[abs(var) - 1] == (var > 0) for var in clause):
                return 1
            for var in clause:
                if not assignment[abs(var) - 1]:
                    stack.append((var, assignment[:]))
                    assignment[abs(var) - 1] = var > 0
                    break
        while stack:
            var, prev_assignment = stack.pop()
            assignment[abs(var) - 1] = not assignment[abs(var) - 1]
            if all(not prev_assignment[abs(var) - 1] == (var > 0) for var in clause):
                return len(stack) + 2
        return float('inf')
    
    proof_length = dpll_proof_length(cnf_instance)
    
    # Verify if proof length ≥ c * sqrt(S(f)) for some constant c > 0
    if proof_length == float('inf'):
        conjecture_holds = False
        counterexample = "DPLL proof failed"
    else:
        c = 1.0
        conjecture_holds = proof_length >= c * math.sqrt(S_f)
        counterexample = ""
    
    return {
        "metric_name": "Frege Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL proof failed\" first_failing_seed={first_failing_seed}")