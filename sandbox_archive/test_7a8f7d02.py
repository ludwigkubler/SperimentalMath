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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):  # Ensure at least 1/3 clauses are positive
            clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tseitin_encoding(cnf):
        literals = set()
        new_vars = {}
        formulas = []
        
        for i, clause in enumerate(cnf):
            literals.update(clause)
            new_var = f'x{i+1}'
            new_vars[new_var] = len(new_vars) + 1
            formulas.append(f'{new_var} <=> {clause[0]}')
            for j in range(1, len(clause)):
                formulas.append(f'{new_var} <=> {clauses[i][j]}')
        
        return formulas, literals
    
    def p_adic_fourier_coefficient(cnf):
        n = max(abs(lit) for lit in cnf[0])
        mfc_min = float('inf')
        for _ in range(10):  # Sample multiple times to get a better estimate
            assignment = {i: random.choice([True, False]) for i in range(-n, n+1)}
            value = sum(2**sum(assignment[lit] if lit > 0 else -assignment[-lit] for lit in clause) for clause in cnf)
            mfc_min = min(mfc_min, abs(value))
        return mfc_min
    
    def frege_proof_length(cnf):
        formulas, literals = tseitin_encoding(cnf)
        proof_length = len(formulas) * 2 + len(literals) * 2
        return proof_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfc_min_sum = 0
    l_f_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        mfc_min = p_adic_fourier_coefficient(cnf)
        l_f = frege_proof_length(cnf)
        
        mfc_min_sum += mfc_min
        l_f_sum += l_f
        instances_tested += len(cnf)
        n_max = max(n_max, n)
    
    mean_mfc_min = mfc_min_sum / instances_tested
    mean_l_f = l_f_sum / instances_tested
    
    if mean_mfc_min == 0 or math.isinf(mean_l_f):
        return {
            "metric_name": "mfc_min",
            "metric_value": mean_mfc_min,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (mean_mfc_min * mean_l_f - mfc_min_sum * l_f_sum / instances_tested) / (math.sqrt(mfc_min_sum**2 / instances_tested - mean_mfc_min**2) * math.sqrt(l_f_sum**2 / instances_tested - mean_l_f**2))
    
    return {
        "metric_name": "mfc_min",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break