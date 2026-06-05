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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            for j in range(i):
                clauses.append([f'~{variables[i]}', f'{variables[j]}'])
                clauses.append([f'~{variables[j]}', f'{variables[i]}'])
        return clauses

    def boolean_lattice(clauses):
        lattice = {}
        for clause in clauses:
            for var in clause:
                if var.startswith('~'):
                    lattice[var[1:]] = 0
                else:
                    lattice[var] = 1
        return lattice

    def min_rank_k_theory(lattice):
        n = len(lattice)
        rank = 0
        while True:
            independent_vars = []
            for var in lattice:
                if all(lattice[var] != lattice[other_var] for other_var in lattice if other_var != var):
                    independent_vars.append(var)
                    break
            if not independent_vars:
                break
            rank += 1
            for var in independent_vars:
                del lattice[var]
        return rank

    def communication_complexity_rank(clauses):
        n = len(clauses)
        max_clauses = 0
        for i in range(n):
            clauses[i] = [f'~{clause}' if clause.startswith('~') else f'{clause}' for clause in clauses[i]]
            max_clauses = max(max_clauses, sum(1 for clause in clauses[i] if not clause.startswith('~')))
        return math.ceil(math.log2(max_clauses))

    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    lattice = boolean_lattice(clauses)
    min_rank_kth = min_rank_k_theory(lattice)
    R_phi = communication_complexity_rank(clauses)

    if min_rank_kth == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_rank_K_theory_is_zero"
        }

    log_min_rank_kth = math.log2(min_rank_kth)
    within_bound = abs(R_phi - log_min_rank_kth) <= 0.1 * log_min_rank_kth

    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": R_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": within_bound,
        "counterexample": "" if within_bound else f"R(φ) = {R_phi}, log(min_rank(K(L(φ)))) = {log_min_rank_kth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'] != 'mapping_undefined')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")