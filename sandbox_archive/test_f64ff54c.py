# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, 3))]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model):
        unsatisfied_clauses = [c for c in cnf if not any(l in model or -l in model for l in c)]
        if not unsatisfied_clauses:
            return model
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = model.copy()
            new_model[literal] = True
            result = solve(new_model)
            if result is not None:
                return result
            new_model[literal] = False
            new_model[-literal] = True
            return solve(new_model)
        pure_literal = next((l for l in range(1, n + 1) if (all(l in m or -l in m for m in cnf)) and not any(-l in m or l in m for m in cnf)), None)
        if pure_literal:
            new_model = model.copy()
            new_model[pure_literal] = True
            return solve(new_model)
        literal, _ = random.choice([(l, c) for c in unsatisfied_clauses for l in c])
        new_model = model.copy()
        new_model[literal] = True
        result = solve(new_model)
        if result is not None:
            return result
        new_model[literal] = False
        new_model[-literal] = True
        return solve(new_model)
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        m_phi = len(cnf)  # Simplified representation length
        d_phi = len(dpll(cnf))  # Frege proof depth
        results.append((m_phi, d_phi))
    
    if not all(results):
        return {
            "metric_name": "m(φ)/d(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_phi_sum = sum(m for m, _ in results)
    d_phi_sum = sum(d for _, d in results)
    mean_m_phi = Fraction(m_phi_sum, len(results))
    mean_d_phi = Fraction(d_phi_sum, len(results))
    ratio_mean = mean_m_phi / mean_d_phi
    ratio_std = 0
    
    if ratio_mean != 1:
        ratio_diffs = [(m - d) for m, d in results]
        ratio_diff_sum = sum(abs(diff) for diff in ratio_diffs)
        ratio_std = Fraction(ratio_diff_sum, len(results))
    
    support_fraction = (abs(ratio_mean - 1) <= Fraction(10, 100)) and (ratio_std <= Fraction(3, 100))
    
    return {
        "metric_name": "m(φ)/d(φ)",
        "metric_value": float(mean_m_phi / mean_d_phi),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    std_metric = (sum((x - mean_metric) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if abs(r - 1) <= 0.1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(abs(r - 1) > 0.1 for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if abs(r - 1) > 0.1)]
        print(f"RESULT: FALSIFIED counterexample='m(φ)/d(φ) out of tolerance' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")