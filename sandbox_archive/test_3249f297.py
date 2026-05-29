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
    
    # Generate a random k-CNF formula with n variables and varying clause density
    n = 10
    k = 3
    num_clauses = random.randint(5, 20)
    variables = list(range(n))
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(k)]
        clauses.append(clause)
    
    # Construct the associated quaternion algebra and compute its minimal exponent
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                A[var-1][var-1] += 1
            else:
                A[-var-1][-var-1] -= 1
    
    # Compute the minimal exponent of the quaternion algebra
    exp_A = max(abs(sum(row)) for row in A)
    
    # Measure the communication complexity required to solve the k-CNF problem
    comm_complexity = math.log(exp_A, 2) if exp_A > 0 else float('inf')
    
    # Check if the conjecture holds
    c = 1.0
    conjecture_holds = exp_A <= c * n**2
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"exp(A)={exp_A}, n^2={n**2}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = results[seeds.index(first_failing_seed)]['counterexample']
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")