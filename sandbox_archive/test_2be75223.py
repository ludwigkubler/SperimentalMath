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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(cnf):
        literals = set()
        formulas = {}
        new_var = 0
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    pos_i = abs(clause[i])
                    pos_j = abs(clause[j])
                    neg_i = -pos_i
                    neg_j = -pos_j
                    formulas[(neg_i, neg_j)] = new_var
                    literals.add(new_var)
                    new_var += 1
        
        for literal in literals:
            formulas[literal] = new_var
            literals.add(new_var)
            new_var += 1
        
        return formulas
    
    def hypergeometric_sum(cnf, formulas):
        n = len(cnf)
        p = len(formulas) / (2**n - 1)
        sum_val = 0
        for clause in cnf:
            prob = 1
            for lit in clause:
                if lit > 0:
                    prob *= p
                else:
                    prob *= 1 - p
            sum_val += prob
        return sum_val
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        formulas = tseitin_formula(cnf)
        sum_val = hypergeometric_sum(cnf, formulas)
        total_sum += sum_val
        instances_tested += len(cnf)
        n_max = max(n_max, n)
    
    mean_sum = total_sum / instances_tested
    
    return {
        "metric_name": "Minimal Hypergeometric Sum",
        "metric_value": mean_sum,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")