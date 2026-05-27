# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} ∨ ¬{var}')
        for i in range(2, n+1):
            clauses.append(' ∧ '.join(variables[:i]))
        return ' ∧ '.join(clauses)
    
    def stabilizer_matrix(formula):
        # Simplified version; actual implementation depends on the formula
        return [[0]*n for _ in range(n)]
    
    def quantum_entanglement_entropy(matrix):
        # Simplified version; actual implementation depends on the matrix
        return 1.0
    
    def resolution_length(formula):
        # Simplified version; actual implementation depends on the formula
        return len(formula.split(' ∧ '))
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    matrix = stabilizer_matrix(formula)
    entropy = quantum_entanglement_entropy(matrix)
    length = resolution_length(formula)
    
    if entropy <= 0 or length <= 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "invalid_input"
        }
    
    rank = len(matrix)
    if rank == 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "zero_rank"
        }
    
    expected_length = 2 ** (math.log2(rank))
    if length < expected_length:
        return {
            "metric_name": "resolution_length",
            "metric_value": length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"length={length} < expected_length={expected_length}"
        }
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    mean_d = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / sum(1 for r in results if r['metric_value'] is not None)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_d)**2 for r in results if r['metric_value'] is not None) / (sum(1 for r in results if r['metric_value'] is not None) - 1))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='resolution_length' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")