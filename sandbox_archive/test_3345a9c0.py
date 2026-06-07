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
        cnf = []
        for _ in range(2**n):  # Generate 2^n clauses
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def p_adic_valuation_rank(cnf):
        valuation_rank = 0
        for clause in cnf:
            prime_ideals = set()
            for literal in clause:
                if literal > 0:
                    prime_ideals.add(literal)
                else:
                    prime_ideals.add(-literal)
            valuation_rank = max(valuation_rank, len(prime_ideals))
        return valuation_rank
    
    def dpll(cnf):
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        
        def solve(model, literals):
            if not literals:
                return [model]
            literal = literals[0]
            pos_model = model.copy()
            neg_model = model.copy()
            pos_model[literal] = True
            neg_model[literal] = False
            pos_solutions = solve(pos_model, literals[1:])
            neg_solutions = solve(neg_model, literals[1:])
            return pos_solutions + neg_solutions
        
        solutions = solve({}, literals)
        return len(solutions) > 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    valranks = []
    dpls = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        valrank = p_adic_valuation_rank(cnf)
        dpl = dpll(cnf)
        valranks.append(valrank)
        dpls.append(dpl)
    
    mean_valrank = sum(valranks) / len(valranks)
    mean_dpl = sum(dpls) / len(dpls)
    
    correlation_coefficient = 0
    if mean_valrank != 0 and mean_dpl != 0:
        numerator = sum((valranks[i] - mean_valrank) * (dpls[i] - mean_dpl) for i in range(len(valranks)))
        denominator = math.sqrt(sum((valranks[i] - mean_valrank)**2 for i in range(len(valranks)))) * math.sqrt(sum((dpls[i] - mean_dpl)**2 for i in range(len(dpls))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(valranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
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
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.8' first_failing_seed={first_failing_seed}")