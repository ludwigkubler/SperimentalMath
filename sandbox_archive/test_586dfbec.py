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
        instance = [random.choice([0, 1]) for _ in range(n)]
        return instance
    
    def encode_in_noncommutative_matrices(instance):
        n = len(instance)
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if instance[i] == 1 and instance[j] == 1:
                    A[i][j] = 1
                    B[i][j] = 1
        
        return A, B
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        
        return C
    
    def l2_norm(matrix):
        n = len(matrix)
        norm = 0.0
        
        for i in range(n):
            for j in range(n):
                norm += matrix[i][j] ** 2
        
        return math.sqrt(norm)
    
    n = random.randint(5, 40)
    instance = generate_disjointness_instance(n)
    A, B = encode_in_noncommutative_matrices(instance)
    C = matrix_multiplication(A, B)
    norm = l2_norm(C)
    
    lower_bound = math.sqrt(n)
    if norm < lower_bound:
        return {
            "metric_name": "Noncommutative L^2-norm",
            "metric_value": norm,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Lower bound not met: {norm} < {lower_bound}"
        }
    
    return {
        "metric_name": "Noncommutative L^2-norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Lower bound not met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")