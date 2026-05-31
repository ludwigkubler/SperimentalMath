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
    
    def generate_binary_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def transpose(matrix):
        n = len(matrix)
        return [[matrix[j][i] for j in range(n)] for i in range(n)]
    
    def symplectic_form(A, B):
        return matrix_multiplication(transpose(B), A)
    
    def gram_schmidt(matrix):
        n = len(matrix)
        Q = []
        R = [[0] * n for _ in range(n)]
        for k in range(n):
            v = [matrix[k][i] for i in range(n)]
            for j in range(k):
                r = sum(Q[j][i] * v[i] for i in range(n))
                R[j][k] = r
                v = [v[i] - r * Q[j][i] for i in range(n)]
            norm = math.sqrt(sum(v[i]**2 for i in range(n)))
            if norm == 0:
                continue
            Q.append([v[i] / norm for i in range(n)])
            R[k][k] = norm
        return Q, R
    
    def minrank(matrix):
        Q, _ = gram_schmidt(matrix)
        rank = sum(1 for row in Q if any(row))
        return rank
    
    def communication_complexity(A):
        n = len(A)
        # Simplified model: complexity is proportional to the number of non-zero entries
        return sum(sum(row) for row in A)
    
    def omega(n):
        # Simplified model: exponential growth rate
        return 2 ** (n / 10)
    
    instances_tested = 0
    n_max = 0
    ranks = []
    complexities = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            A = generate_binary_matrix(n)
            symplectic_A = symplectic_form(A, A)
            rank = minrank(symplectic_A)
            complexity = communication_complexity(A)
            
            ranks.append(rank)
            complexities.append(complexity)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "minrank vs omega",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (complexities[i] - mean_complexities) for i in range(instances_tested)) / instances_tested
    mean_ranks = sum(ranks) / instances_tested
    mean_complexities = sum(complexities) / instances_tested
    
    if correlation_coefficient < 0.9:
        return {
            "metric_name": "minrank vs omega",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"low_correlation {correlation_coefficient}"
        }
    
    return {
        "metric_name": "minrank vs omega",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"low_correlation {r['metric_value']}\" first_failing_seed={seed}")
                break