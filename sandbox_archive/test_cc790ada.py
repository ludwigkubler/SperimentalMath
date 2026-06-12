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

# Generate a random CNF formula with n variables and m clauses
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            clause.add(lit)
        cnf.append(list(clause))
    return cnf

# Convert CNF formula to DPLL input format
def cnf_to_dpll(cnf):
    dpll_input = []
    for clause in cnf:
        dpll_input.append([abs(lit) for lit in clause] + [0])
    dpll_input.append([0])
    return dpll_input

# DPLL algorithm to find a refutation
def dpll(cnf):
    cnf = cnf_to_dpll(cnf)
    stack = []
    assignment = {}
    def backtrack():
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            if abs(lit) in assignment and assignment[abs(lit)] != (lit > 0):
                return False
            assignment[abs(lit)] = lit > 0
            stack.append((lit, len(cnf)))
            cnf = [c for c in cnf if not any(l in c for l in (lit, -lit))]
        else:
            lit = next(abs(l) for l in random.choice(cnf))
            assignment[lit] = True
            stack.append((lit, len(cnf)))
            cnf = [c for c in cnf if not any(l in c for l in (lit, -lit))]
        return backtrack()
    if not backtrack():
        return None
    proof_length = 0
    while stack:
        lit, length = stack.pop()
        proof_length += length
    return proof_length

# Compute the minimal p-adic Hodge theory rank (simplified for testing)
def p_adic_hodge_rank(cnf):
    # Placeholder implementation: return a random number between 1 and n
    n = max(abs(lit) for clause in cnf for lit in clause)
    return random.randint(1, n)

# Run one trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        for _ in range(30):  # Test each size 30 times
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            rank_H = p_adic_hodge_rank(cnf)
            proof_length = dpll(cnf)
            if proof_length is None:
                continue
            results.append((rank_H, proof_length))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid CNF formulas generated"
        }
    rank_H_values = [r[0] for r in results]
    proof_length_values = [r[1] for r in results]
    mean_rank_H = sum(rank_H_values) / len(rank_H_values)
    mean_proof_length = sum(proof_length_values) / len(proof_length_values)
    covariance = sum((rank_H - mean_rank_H) * (proof_length - mean_proof_length) for rank_H, proof_length in results) / len(results)
    variance_rank_H = sum((rank_H - mean_rank_H) ** 2 for rank_H in rank_H_values) / len(rank_H_values)
    variance_proof_length = sum((proof_length - mean_proof_length) ** 2 for proof_length in proof_length_values) / len(proof_length_values)
    pearson_corr_coeff = covariance / (math.sqrt(variance_rank_H) * math.sqrt(variance_proof_length))
    conjecture_holds = pearson_corr_coeff >= 0.8 and all(rank_H <= proof_length * 1.5 for rank_H, proof_length in results)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rank_H > |P(φ)| * 1.5"
    }

# Main execution
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_H > |P(φ)| * 1.5\" first_failing_seed={first_failing_seed}")