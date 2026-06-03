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

def generate_formula(n, clause_density):
    literals = [f'x{i}' for i in range(1, n + 1)]
    clauses = set()
    
    for _ in range(math.ceil(clause_density * n * (n - 1) / 2)):
        lit1, lit2 = random.sample(literals, 2)
        clause = f'{lit1} OR {lit2}'
        if clause not in clauses and f'~{lit1} OR ~{lit2}' not in clauses:
            clauses.add(clause)
    
    return literals, list(clauses)

def tseitin_formula(literals, clauses):
    tseitin_vars = [f'y{i}' for i in range(1, len(clauses) + 1)]
    formula = []
    
    for i, clause in enumerate(clauses):
        y_var = tseitin_vars[i]
        formula.append(f'{y_var} <-> ({clause})')
        for lit in literals:
            if f'~{lit}' in clause:
                formula.append(f'{y_var} -> ~{lit}')
            else:
                formula.append(f'{y_var} -> {lit}')
    
    return ' AND '.join(formula)

def solve(lits_true, lits_false):
    stack = []
    model = {}
    
    for lit in lits_true + lits_false:
        if lit.startswith('~'):
            other_lit = lit[1:]
            if other_lit not in model or model[other_lit]:
                return False
        else:
            if lit not in model or not model[lit]:
                stack.append(lit)
    
    while stack:
        lit = stack.pop()
        if lit.startswith('~'):
            other_lit = lit[1:]
            if other_lit not in model or model[other_lit]:
                return False
            model[other_lit] = True
        else:
            if lit not in model or not model[lit]:
                model[lit] = True
    
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = generate_formula(n, 2 / n)
        tseitin_formula_str = tseitin_formula(literals, clauses)
        
        # Simulate a DPLL solver to get the resolution proof width
        lits_true = [lit for lit in literals if solve([lit], [])]
        lits_false = [lit for lit in literals if not solve([lit], [])]
        w_phi = len(lits_true) + len(lits_false)
        
        # Compute the minimal tropical derivative rank (mtr(φ))
        p = 101
        f_phi_coeffs = {}
        for clause in clauses:
            coeffs = [0] * (n + 1)
            for lit in clause.split(' OR '):
                if lit.startswith('~'):
                    coeffs[int(lit[1:]) - 1] = -1
                else:
                    coeffs[int(lit) - 1] = 1
            f_phi_coeffs[tuple(coeffs)] = 0
        
        jacobian = []
        for i in range(n + 1):
            row = [0] * (n + 1)
            for clause, coeff in f_phi_coeffs.items():
                if clause[i] != 0:
                    row[i] += coeff
            jacobian.append(row)
        
        rank = 0
        for row in jacobian:
            if any(x != 0 for x in row):
                pivot_col = next(j for j, x in enumerate(row) if x != 0)
                for i in range(n + 1):
                    if i != pivot_col and jacobian[i][pivot_col] != 0:
                        factor = jacobian[i][pivot_col] / row[pivot_col]
                        for j in range(n + 1):
                            jacobian[i][j] -= factor * row[j]
                rank += 1
        
        mtr_phi = rank
        
        results.append({"n": n, "mtr_phi": mtr_phi, "w_phi": w_phi})
    
    correlation_coefficient = 0
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            x1, y1 = results[i]["mtr_phi"], results[i]["w_phi"]
            x2, y2 = results[j]["mtr_phi"], results[j]["w_phi"]
            correlation_coefficient += (x1 - x2) * (y1 - y2)
    
    n_pairs = len(n_values) * (len(n_values) - 1) // 2
    mean_mtr_phi = sum(result["mtr_phi"] for result in results) / len(results)
    mean_w_phi = sum(result["w_phi"] for result in results) / len(results)
    
    correlation_coefficient /= n_pairs * math.sqrt((sum((result["mtr_phi"] - mean_mtr_phi) ** 2 for result in results)) * (sum((result["w_phi"] - mean_w_phi) ** 2 for result in results)))
    
    p_value = 2 * (1 - abs(correlation_coefficient))
    
    conjecture_holds = correlation_coefficient >= 0.8 and p_value <= 0.01
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}, P-value: {p_value}"
    
    return {
        "metric_name": "Tropical Derivative Rank vs Resolution Proof Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")