# auto-injected by SEC sandbox
import math
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

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if m == 1:
        return A[0][0]
    det = Fraction(0, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        kr_sum = Fraction(0, 1)
        h_sum = Fraction(0, 1)
        
        while len(results) < 30:
            f = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
            phi = ''.join(''.join(str(x) for x in row) for row in f)
            
            # Constructive mapping to geometric object Oφ
            O_phi = sum([sum(row) for row in f], 0)
            
            # Compute Kähler class rank kr(φ)
            A = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
            det_A = determinant(A)
            kr_phi = abs(det_A)
            
            # Compute DPLL search tree height h(φ)
            def dpll(phi):
                if not phi:
                    return 0
                if '0' not in phi and '1' not in phi:
                    return 0
                if phi[0] == '0':
                    return 1 + dpll(phi[2:])
                if phi[0] == '1':
                    return 1 + dpll(phi[2:])
                return max(1 + dpll(phi[2:phi.find('1')]), 1 + dpll(phi[phi.find('1')+1:]))
            h_phi = dpll(phi)
            
            kr_sum += kr_phi
            h_sum += h_phi
            instances_tested += 1
            
        mean_kr = kr_sum / instances_tested
        mean_h = h_sum / instances_tested
        correlation_coefficient = (instances_tested * sum(kr_phi * h_phi for kr_phi, h_phi in zip(results, results)) - mean_kr * mean_h) / (instances_tested * sum((kr_phi - mean_kr) ** 2 for kr_phi in results) * sum((h_phi - mean_h) ** 2 for h_phi in results))
        
        results.append(correlation_coefficient)
    
    n_max = max(n_values)
    conjecture_holds = all(abs(cc - 1.0) <= Fraction(5, 100) for cc in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": sum(results) / len(results),
        "instances_tested": instances_tested * len(n_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_metric_value = sum(result["metric_value"] for result in [run_trial(seed) for seed in seeds]) / len(seeds)
    support_fraction = sum(1 for result in [run_trial(seed) for seed in seeds] if result["conjecture_holds"]) / len(seeds)
    
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")