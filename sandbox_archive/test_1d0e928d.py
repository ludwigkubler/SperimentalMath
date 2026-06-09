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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(d) for c in clause for d in clauses[-1]):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(assignment, literals):
            if not literals:
                return True
            var = literals[0]
            pos_var, neg_var = abs(var), -abs(var)
            if pos_var in assignment and assignment[pos_var] != (var > 0):
                return False
            if neg_var in assignment and assignment[neg_var] != (var < 0):
                return False
            
            assignment[pos_var] = var > 0
            if solve(assignment, literals[1:]):
                return True
            del assignment[pos_var]
            
            assignment[neg_var] = var < 0
            if solve(assignment, literals[1:]):
                return True
            del assignment[neg_var]
            
            return False
        
        assignment = {}
        literals = [i for i in range(1, len(cnf) + 1)]
        return solve(assignment, literals)
    
    n_max = 40
    instances_tested = 0
    m_phi_total = 0
    d_phi_total = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            m_phi = len(cnf)  # Minimal representation length (number of clauses)
            d_phi = len(dpll(cnf))  # Frege proof depth
            
            if m_phi == 0 or d_phi == 0:
                continue
            
            instances_tested += 1
            m_phi_total += m_phi
            d_phi_total += d_phi
    
    mean_m_phi = Fraction(m_phi_total, instances_tested)
    mean_d_phi = Fraction(d_phi_total, instances_tested)
    ratio_mean = (mean_m_phi / mean_d_phi).limit_denominator()
    
    if ratio_mean.numerator == 1 and ratio_mean.denominator == 1:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Ratio of m(φ)/d(φ) is {ratio_mean}, expected ≈ 1.0"
    
    return {
        "metric_name": "m_phi_over_d_phi",
        "metric_value": float(m_phi_total / instances_tested),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")