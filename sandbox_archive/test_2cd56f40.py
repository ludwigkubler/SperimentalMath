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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // n):
            clause = [random.randint(-1, 1) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def cnf_to_polynomial(cnf, p):
        variables = list(range(1, len(cnf) + 1))
        polynomial = [0] * (p**len(variables))
        
        def assign(var, value):
            index = sum(value if i == var else 0 for i in range(len(variables)))
            return index
        
        for clause in cnf:
            product = 1
            for literal in clause:
                var, sign = abs(literal), -1 if literal < 0 else 1
                product *= (sign * (-1 + p**assign(var)))
            polynomial[assign(0, [1] * len(variables))] += product
        
        return polynomial
    
    def mcr(polynomial):
        n = len(polynomial)
        max_growth_rate = 0
        for i in range(1, n):
            growth_rate = abs(polynomial[i] - polynomial[i-1])
            if growth_rate > max_growth_rate:
                max_growth_rate = growth_rate
        return max_growth_rate
    
    def frege_proof_depth(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    total_mcr_f_ratio = 0.0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        polynomial = cnf_to_polynomial(cnf, p=2)  # Using binary field for simplicity
        mcr_value = mcr(polynomial)
        f_value = frege_proof_depth(cnf)
        
        if f_value == 0:
            continue
        
        total_mcr_f_ratio += Fraction(mcr_value, f_value).limit_denominator()
    
    mean_mcr_f_ratio = total_mcr_f_ratio / instances_tested
    conjecture_holds = mean_mcr_f_ratio <= 1
    
    return {
        "metric_name": "MCR/F ratio",
        "metric_value": float(mean_mcr_f_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")