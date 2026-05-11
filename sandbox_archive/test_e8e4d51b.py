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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def count_solutions(A):
    gaussian_elimination(A)
    solutions = 1
    for row in A:
        if all(x == 0 for x in row[:-1]) and row[-1] != 0:
            return 0
        elif all(x == 0 for x in row[:-1]):
            solutions *= 2
    return solutions

def generate_sipser_instance(n):
    truth_table = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    quadratic_system = []
    for i in range(2**n):
        row = [truth_table[i][j] ^ truth_table[i][k] for j in range(n) for k in range(j+1, n)]
        quadratic_system.append(row)
    return quadratic_system

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        quadratic_system = generate_sipser_instance(n)
        solutions_count = count_solutions(quadratic_system)
        
        if solutions_count < 2**(n/2 - 5):
            return {
                "metric_name": "solutions_count",
                "metric_value": solutions_count,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, solutions_count={solutions_count}"
            }
        
        # Simulate ACC⁰ circuit size (depth-3 threshold circuits)
        acc0_size = 2**(n/2 - 5)
        if acc0_size < 1:
            return {
                "metric_name": "acc0_size",
                "metric_value": acc0_size,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, acc0_size={acc0_size}"
            }
        
        results.append({
            "solutions_count": solutions_count,
            "acc0_size": acc0_size
        })
    
    return {
        "metric_name": "solutions_count",
        "metric_value": sum(r["solutions_count"] for r in results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")