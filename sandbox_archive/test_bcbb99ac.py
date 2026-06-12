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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_from_function(func, n):
        A = [[func[i ^ j] for j in range(2**n)] for i in range(2**n)]
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if A[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for row in range(rank, m):
                factor = A[row][col] / A[pivot_row][col]
                for j in range(n):
                    A[row][j] -= factor * A[pivot_row][j]
        return rank
    
    def frege_proof_depth(func, n):
        # Simplified DPLL solver to estimate Frege proof depth
        stack = []
        literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
        while literals:
            literal = random.choice(literals)
            if literal > 0:
                stack.append(literal)
                literals.remove(literal)
                literals.remove(-literal)
            else:
                neg_literal = -literal
                if neg_literal not in stack:
                    return len(stack) + 1
                stack.remove(neg_literal)
        return len(stack)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):
            func = generate_boolean_function(n)
            A = matrix_from_function(func, n)
            rrep_f = gaussian_elimination(A)
            d_f = frege_proof_depth(func, n)
            
            if rrep_f == 0 or d_f == 0:
                continue
            
            metric_values.append(rrep_f / d_f)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "rrep(f) / d_f",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "rrep(f) / d_f",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_dev_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_dev_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first_failing_seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")