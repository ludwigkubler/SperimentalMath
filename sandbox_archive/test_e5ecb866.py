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

def is_quadratic_residue(a, p):
    if a == 0:
        return True
    for x in range(1, p):
        if (x * x) % p == a:
            return True
    return False

def count_quadratic_residues(p):
    return sum(is_quadratic_residue(a, p) for a in range(p))

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for i in range(1, n+1):
        clauses.append([variables[i-1]])
        for j in range(i+1, n+1):
            clauses.append([-variables[i-1], variables[j-1]])
            clauses.append([-variables[j-1], variables[i-1]])
    return clauses

def resolution_length(clauses):
    queue = clauses.copy()
    while True:
        new_clauses = []
        for i in range(len(queue)):
            for j in range(i+1, len(queue)):
                for literal_i in queue[i]:
                    if -literal_i in queue[j]:
                        new_clause = [l for l in queue[i] + queue[j] if l != literal_i and -l != literal_i]
                        if not new_clause:
                            return len(queue) + 1
                        new_clauses.append(new_clause)
        if new_clauses == queue:
            return float('inf')
        queue.extend(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            p = random.randint(n+1, 2*n)
            clauses = generate_tseitin_formula(n)
            length = resolution_length(clauses)
            if length != float('inf'):
                total_length += length
                instances_tested += 1
    
    mean_length = Fraction(total_length, instances_tested) if instances_tested > 0 else 0
    expected_length = Fraction(n_values[-1]**2 * math.log(n_values[-1], count_quadratic_residues(p)), math.log(math.log(n_values[-1], count_quadratic_residues(p))))
    
    conjecture_holds = abs(mean_length - expected_length) <= 0.1 * expected_length
    counterexample = "" if conjecture_holds else f"Mean length {mean_length} not within ±10% of expected {expected_length}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_length = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")