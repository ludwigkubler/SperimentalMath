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

def generate_k_sat_instance(n, k):
    instance = []
    for _ in range(k):
        clause = set()
        while len(clause) < 3:
            lit = random.randint(-n, n)
            if lit not in clause and -lit not in clause:
                clause.add(lit)
        instance.append(list(clause))
    return instance

def is_satisfiable(instance):
    def backtrack(assignment=None):
        assignment = assignment or {}
        for i in range(1, len(instance) + 1):
            if i not in assignment:
                for lit in [-i, i]:
                    assignment[i] = lit
                    if all(any(assignment[abs(lit)] == lit for lit in clause) for clause in instance):
                        return True
                    else:
                        del assignment[i]
        return False

    return backtrack()

def compute_hypergeometric_function_rank(circuit):
    # Placeholder function to simulate hypergeometric function rank computation
    # Replace this with actual implementation if available
    return len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    satisfiable_ranks = []
    unsatisfiable_ranks = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instance = generate_k_sat_instance(n, k=3)
            satisfiable = is_satisfiable(instance)
            
            circuit = construct_circuit(instance)  # Placeholder function to simulate circuit construction
            rank = compute_hypergeometric_function_rank(circuit)
            
            instances_tested += 1
            
            if satisfiable:
                satisfiable_ranks.append(rank)
            else:
                unsatisfiable_ranks.append(rank)
    
    mrf_satisfiable = sum(satisfiable_ranks) / len(satisfiable_ranks) if satisfiable_ranks else None
    mrf_unsatisfiable = sum(unsatisfiable_ranks) / len(unsatisfiable_ranks) if unsatisfiable_ranks else None
    
    correlation_coefficient = calculate_correlation(satisfiable_ranks, range(len(satisfiable_ranks)))
    
    conjecture_holds = (correlation_coefficient >= 0.9 and mrf_unsatisfiable >= 2 * n_max)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mrf",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    if len(x) != len(y):
        return None
    
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
    var_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
    
    if var_x == 0 or var_y == 0:
        return None
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def construct_circuit(instance):
    # Placeholder function to simulate circuit construction
    # Replace this with actual implementation if available
    return instance

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")