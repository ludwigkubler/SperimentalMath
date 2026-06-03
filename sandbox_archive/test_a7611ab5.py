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
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for lit in literals:
            clauses.append([lit])
        for i in range(n-1):
            clauses.append([f'x{i}', f'x{i+1}'])
        return literals, clauses
    
    def clause_indicator_polynomial(literals, clauses):
        n = len(literals)
        poly = [0] * (n + 1)
        for clause in clauses:
            term = 1
            for lit in clause:
                if lit.startswith('x'):
                    idx = int(lit[1:]) - 1
                    term *= (1 - 2 * random.randint(0, 1))
                else:
                    idx = int(lit[1:]) - 1
                    term *= (1 + 2 * random.randint(0, 1))
            poly[-1] += term
        return poly
    
    def sum_of_abs_roots(poly):
        n = len(poly)
        if n == 1:
            return abs(poly[0])
        roots = []
        for i in range(n-1):
            a, b = poly[i], poly[i+1]
            root = -b / (2 * a)
            roots.append(root)
        return sum(abs(root) for root in roots)
    
    def frege_proof_length(formula):
        literals, clauses = formula
        stack = []
        for lit in literals:
            stack.append(lit)
        proof_length = 0
        while stack:
            lit = stack.pop()
            if lit.startswith('x'):
                idx = int(lit[1:]) - 1
                clause = [f'x{i}' if i != idx else f'-x{i}' for i in range(1, len(literals)+1)]
                clauses.append(clause)
                proof_length += 2
            else:
                neg_lit = lit[1:]
                idx = int(neg_lit[1:]) - 1
                clause = [f'x{i}' if i != idx else f'-x{i}' for i in range(1, len(literals)+1)]
                clauses.append(clause)
                proof_length += 2
        return proof_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n)
        poly = clause_indicator_polynomial(literals, clauses)
        abs_root_sum = sum_of_abs_roots(poly)
        proof_length = frege_proof_length((literals, clauses))
        results.append({
            "n": n,
            "abs_root_sum": abs_root_sum,
            "proof_length": proof_length
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    abs_root_sums = [result["abs_root_sum"] for result in results]
    proof_lengths = [result["proof_length"] for result in results]
    
    mean_abs_root_sum = sum(abs_root_sums) / len(abs_root_sums)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    
    covariance = sum((abs_root_sums[i] - mean_abs_root_sum) * (proof_lengths[i] - mean_proof_length) for i in range(len(results))) / len(results)
    variance_x = sum((abs_root_sums[i] - mean_abs_root_sum) ** 2 for i in range(len(results))) / len(results)
    variance_y = sum((proof_lengths[i] - mean_proof_length) ** 2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['n']}, abs_root_sum={result['abs_root_sum']}, proof_length={result['proof_length']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break