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
    
    def boolean_to_coxeter_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if f[i] != f[j]:
                    matrix[i][j] = matrix[j][i] = 2
        return matrix
    
    def min_order(matrix):
        n = len(matrix) - 1
        identity = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            identity[i][i] = 1
        
        def multiply(A, B):
            result = [[0] * (n + 1) for _ in range(n + 1)]
            for i in range(n + 1):
                for j in range(n + 1):
                    for k in range(n + 1):
                        result[i][j] += A[i][k] * B[k][j]
            return result
        
        def subtract(A, B):
            return [[A[i][j] - B[i][j] for j in range(n + 1)] for i in range(n + 1)]
        
        def add(A, B):
            return [[A[i][j] + B[i][j] for j in range(n + 1)] for i in range(n + 1)]
        
        def is_identity(M):
            for i in range(n + 1):
                for j in range(n + 1):
                    if M[i][j] != (i == j):
                        return False
            return True
        
        order = 0
        current_matrix = matrix[:]
        while not is_identity(current_matrix):
            current_matrix = multiply(current_matrix, matrix)
            order += 1
        return order
    
    def circuit_complexity(f):
        n = int(math.log2(len(f)))
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            return 2 * circuit_complexity([f[i] ^ f[j] for i in range(n) for j in range(i + 1, n)])
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        Phi_f = min_order(boolean_to_coxeter_matrix(f))
        cc_f = circuit_complexity(f)
        results.append((Phi_f, cc_f))
    
    mean_cc = sum(cc for _, cc in results) / len(results)
    std_dev = math.sqrt(sum((cc - mean_cc)**2 for _, cc in results) / len(results))
    correlation_coefficient = sum((Phi * (cc - mean_cc)) for Phi, cc in results) / (len(results) * std_dev * mean_cc)
    
    return {
        "metric_name": "Circuit Complexity",
        "metric_value": mean_cc,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_coefficient < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")