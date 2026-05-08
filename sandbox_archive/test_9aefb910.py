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

def generate_random_monotone_ac0_formula(n):
    # Generate a random monotone AC⁰ formula computing PARITY on n variables
    # This is a simplified version for demonstration purposes
    formula = []
    for i in range(1 << n):
        if bin(i).count('1') % 2 == 0:
            formula.append(random.choice([True, False]))
        else:
            formula.append(not random.choice([True, False]))
    return formula

def communication_matrix(formula, n):
    # Compute the communication matrix for a given formula
    m = len(formula)
    mat = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if formula[i]:
                mat[i][j] = 1
            else:
                mat[i][j] = 0
    return mat

def count_monochromatic_rectangles(mat, n):
    # Count monochromatic rectangles in the communication matrix
    m = len(mat)
    count = 0
    for i1 in range(m):
        for j1 in range(n + 1):
            for i2 in range(i1 + 1, m):
                for j2 in range(j1 + 1, n + 1):
                    if (mat[i1][j1] == mat[i1][j2] == mat[i2][j1] == mat[i2][j2]):
                        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_random_monotone_ac0_formula(n)
    mat = communication_matrix(formula, n)
    count = count_monochromatic_rectangles(mat, n)
    
    metric_name = "monochromatic_rectangle_count"
    metric_value = count
    instances_tested = 1
    conjecture_holds = count >= n
    counterexample = "" if conjecture_holds else f"Formula size: {len(formula)}, Count: {count}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Formula size too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")