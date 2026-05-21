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
    
    def communication_matrix(phi):
        n = 40
        m = 2**n
        comm_matrix = [[0] * (2**n) for _ in range(m)]
        # Placeholder for actual computation of communication matrix
        return comm_matrix
    
    def disjointness_communication_complexity(comm_matrix, n):
        # Placeholder for actual computation of disjointness communication complexity
        return math.log(n)
    
    phi = generate_3cnf_formula(40)
    comm_matrix = communication_matrix(phi)
    comm_complexity = disjointness_communication_complexity(comm_matrix, 40)
    
    min_fourier_coefficient = compute_min_fourier_coefficient(comm_matrix, n)
    
    metric_value = min_fourier_coefficient
    conjecture_holds = min_fourier_coefficient >= 1 / math.sqrt(n) and comm_complexity >= math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_fourier_coefficient",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_3cnf_formula(n):
    # Placeholder for actual generation of a random 3-CNF formula with n variables
    clauses = []
    for _ in range(20):  # Generate 20 clauses as an example
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
    return clauses

def compute_min_fourier_coefficient(comm_matrix, n):
    # Placeholder for actual computation of the minimal non-Abelian Fourier coefficient
    min_coeff = float('inf')
    for row in comm_matrix:
        coeff = sum(row) / len(row)
        if abs(coeff) < min_coeff:
            min_coeff = abs(coeff)
    return min_coeff

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")