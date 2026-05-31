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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(coeff) != 1 for coeff in clause):
                clauses.append(clause)
        return clauses
    
    def dpll_path_length(clauses):
        stack = []
        assignment = {}
        def solve():
            if not clauses:
                return True
            literal = find_unassigned_literal(clauses, assignment)
            if literal is None:
                return False
            for value in [True, False]:
                assignment[literal] = value
                new_clauses = filter_clauses(clauses, literal, value)
                if solve():
                    return True
                del assignment[literal]
            return False
        def find_unassigned_literal(clauses, assignment):
            for clause in clauses:
                for literal in clause:
                    if abs(literal) not in assignment:
                        return literal
            return None
        def filter_clauses(clauses, literal, value):
            new_clauses = []
            for clause in clauses:
                if any(abs(lit) == abs(literal) and lit != literal * value for lit in clause):
                    continue
                new_clause = [lit for lit in clause if abs(lit) != abs(literal)]
                if new_clause:
                    new_clauses.append(new_clause)
            return new_clauses
        solve()
        return len(stack)
    
    def local_zeta_function_size(clauses):
        size = 0
        for clause in clauses:
            size += sum(abs(coeff) for coeff in clause)
        return size
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            zeta_size = local_zeta_function_size(clauses)
            dpll_len = dpll_path_length(clauses)
            results.append((zeta_size, dpll_len))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "local_zeta_function_size",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    zetas, dplls = zip(*results)
    mean_zeta = sum(zetas) / len(zetas)
    mean_dpll = sum(dplls) / len(dplls)
    correlation_coefficient = (len(results) * sum(z * d for z, d in zip(zetas, dplls)) - 
                                mean_zeta * sum(dplls) - 
                                mean_dpll * sum(zetas)) / math.sqrt(len(results) * sum((z - mean_zeta)**2 for z in zetas) * sum((d - mean_dpll)**2 for d in dplls))
    mean_abs_diff = sum(abs(z - d) for z, d in zip(zetas, dplls)) / len(zetas)
    
    return {
        "metric_name": "local_zeta_function_size",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")