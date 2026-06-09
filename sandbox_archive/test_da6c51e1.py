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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        if not cnf:
            return True
        if any(len(clause) == 0 for clause in cnf):
            return False
        
        unit_clauses = [clause[0] for clause in cnf if len(clause) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_cnf = []
            for clause in cnf:
                if literal not in clause and -literal not in clause:
                    new_cnf.append([x for x in clause if x != -literal])
            return dpll(new_cnf)
        
        literal = random.choice(cnf[0])
        new_cnf_true = [clause for clause in cnf if literal not in clause and -literal not in clause]
        new_cnf_false = [clause for clause in cnf if literal in clause] + [[-x for x in clause if -x not in clause] for clause in cnf if -literal not in clause]
        
        return dpll(new_cnf_true) or dpll(new_cnf_false)
    
    def tropical_cyclotomic_polynomial(cnf):
        degree = 0
        coefficients = set()
        for clause in cnf:
            degree += len(clause)
            for literal in clause:
                coefficients.add(abs(literal))
        return degree, len(coefficients)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            if not dpll(cnf):
                continue
            
            degree, coefficient_count = tropical_cyclotomic_polynomial(cnf)
            total_metric_value += degree * math.log2(coefficient_count)
            instances_tested += 1
            n_max = max(n_max, n)
            
            if conjecture_holds and degree * math.log2(coefficient_count) > n * math.log2(n):
                conjecture_holds = False
                counterexample = f"n={n}, degree={degree}, coefficient_count={coefficient_count}"
    
    return {
        "metric_name": "tropical_cyclotomic_polynomial_complexity",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")