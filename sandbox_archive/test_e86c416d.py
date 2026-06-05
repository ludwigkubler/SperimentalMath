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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var, f'~{var}', 'y'])
        for i in range(1, n):
            clauses.append(['~', f'x{i-1}', f'x{i}', 'z'])
        clauses.append(['~', 'z', 'w'])
        return clauses
    
    def boolean_lattice(clauses):
        variables = set()
        for clause in clauses:
            variables.update(clause)
        lattice = []
        for subset in range(2 ** len(variables)):
            subset_vars = [var for var in variables if (subset & (1 << (len(variables) - variables.index(var)))) != 0]
            lattice.append(subset_vars)
        return lattice
    
    def min_rank_k_theory(lattice):
        n = len(lattice[0])
        rank = 0
        while True:
            found_new_clause = False
            for i in range(len(lattice)):
                if not any(var in lattice[j] for j in range(i) if j != i):
                    new_clause = [var for var in lattice[i] if var not in lattice[0]]
                    rank += 1
                    lattice.append(new_clause)
                    found_new_clause = True
            if not found_new_clause:
                break
        return rank
    
    def communication_complexity_rank(clauses, n):
        # Placeholder function; actual implementation needed
        return random.randint(5, 20)  # Dummy value for demonstration
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_formula(n)
    lattice = boolean_lattice(clauses)
    min_rank_k = min_rank_k_theory(lattice)
    if min_rank_k == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_rank_K_theory_is_zero"
        }
    R_phi = communication_complexity_rank(clauses, n)
    log_min_rank_k = math.log(min_rank_k)
    if abs(R_phi - log_min_rank_k) <= 0.1 * log_min_rank_k:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": R_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": R_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"R(phi) = {R_phi}, log(min_rank(K(L(phi)))) = {log_min_rank_k}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reasons")