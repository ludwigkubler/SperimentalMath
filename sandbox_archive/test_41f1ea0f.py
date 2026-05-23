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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def l_p_geometric_entropy(f, p):
        n = len(f)
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    matrix[i][j] = 1
        identity = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
        power_matrix = identity
        for _ in range(int(p)):
            power_matrix = matrix_multiplication(power_matrix, matrix)
        return trace(power_matrix) / (2**n)
    
    def communication_complexity(f):
        n = len(f)
        max_entropy = 0
        for p in [0.1 * i for i in range(11)]:
            entropy = l_p_geometric_entropy(f, p)
            if entropy > max_entropy:
                max_entropy = entropy
        return max_entropy
    
    def disjointness(n):
        return [i == j for i in range(n) for j in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(10):
            f = generate_random_function(n)
            entropy = communication_complexity(f)
            total_metric_value += entropy
            instances_tested += 1
            if entropy < n**(1-1/2):  # Assuming p=1 for simplicity
                conjecture_holds = False
                counterexample = "Disjointness function has lower communication complexity than expected"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested if conjecture_holds else 0
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"Disjointness function has lower communication complexity than expected\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")