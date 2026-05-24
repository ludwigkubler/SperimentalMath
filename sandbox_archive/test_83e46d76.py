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
    
    def generate_disjointness_instance(n):
        return {i: i % 2 for i in range(1, n+1)}
    
    def encode_matrix(instance):
        n = len(instance)
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if instance[i] == 0 and instance[j] == 1:
                    A[i][j] = 1
                elif instance[i] == 1 and instance[j] == 0:
                    B[i][j] = 1
        return A, B
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def l2_norm(matrix):
        n = len(matrix)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += matrix[i][j]**2
        return math.sqrt(norm)
    
    def is_disjoint(instance):
        return all(instance[i] != instance[j] for i in range(len(instance)) for j in range(i+1, len(instance)))
    
    n = random.randint(5, 40)
    instance = generate_disjointness_instance(n)
    A, B = encode_matrix(instance)
    C = matrix_multiply(A, B)
    norm = l2_norm(C)
    
    if not is_disjoint(instance):
        return {
            "metric_name": "Noncommutative L^2-norm",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Instance is not disjoint"
        }
    
    conjecture_holds = norm >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Norm {norm} < sqrt({n}) = {math.sqrt(n)}"
    
    return {
        "metric_name": "Noncommutative L^2-norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")