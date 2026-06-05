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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = Fraction(0, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n > 40:
            break
        
        def generate_boolean_function(n):
            return [random.choice([0, 1]) for _ in range(2**n)]
        
        def compute_matroid(M):
            m = len(M)
            rank = 0
            A = [[Fraction(0, 1)] * (m + 1) for _ in range(m + 1)]
            for i in range(m):
                A[i][i] = Fraction(1, 1)
                for j in range(i+1, m):
                    if M[i][j]:
                        A[j][i], A[i][j] = A[i][j], A[j][i]
                        rank += 1
            return rank
        
        def compute_communication_complexity(f):
            n = len(f)
            count = 0
            for i in range(2**n):
                x = [int(b) for b in format(i, f'0{n}b')]
                y = [f[x[j]] for j in range(n)]
                if sum(y) % 2 == 1:
                    count += 1
            return count
        
        def alexander_defect(M):
            rank = compute_matroid(M)
            det = determinant([[Fraction(1, 1)] * (rank + 1) for _ in range(rank + 1)])
            return abs(det)
        
        for _ in range(30):
            f = generate_boolean_function(n)
            M = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
            A = alexander_defect(M)
            r = compute_communication_complexity(f)
            results.append((A, r))
    
    if not results:
        return {
            "metric_name": "Alexander-Defect Invariant and Communication Complexity Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    A_values = [A for A, r in results]
    r_values = [r for A, r in results]
    
    mean_A = sum(A_values) / len(A_values)
    std_A = math.sqrt(sum((x - mean_A) ** 2 for x in A_values) / len(A_values))
    mean_r = sum(r_values) / len(r_values)
    std_r = math.sqrt(sum((x - mean_r) ** 2 for x in r_values) / len(r_values))
    
    correlation_coefficient = sum((A_values[i] - mean_A) * (r_values[i] - mean_r) for i in range(len(A_values))) / (len(A_values) * std_A * std_r)
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(2 * len(A_values) - 2) / 2))
    
    return {
        "metric_name": "Alexander-Defect Invariant and Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(A_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={result['seed']}")
                break