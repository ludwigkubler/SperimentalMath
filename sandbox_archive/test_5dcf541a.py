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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def is_prime(q):
    if q <= 1:
        return False
    for i in range(2, int(q**0.5) + 1):
        if q % i == 0:
            return False
    return True

def generate_projective_plane(q):
    if not is_prime(q):
        raise ValueError("q must be a prime power")
    
    points = list(range(q * (q + 1)))
    lines = []
    
    for i in range(q):
        line = [i]
        for j in range(1, q + 1):
            line.append((i * j) % q)
        lines.append(line)
    
    for i in range(q + 1):
        line = [(q * (q + 1) - i)]
        for j in range(1, q + 1):
            line.append(((q * (q + 1) - i) * j) % q)
        lines.append(line)
    
    return points, lines

def incidence_matrix(points, lines):
    n = len(points)
    M = [[0] * n for _ in range(n)]
    
    for line in lines:
        for point in line:
            M[point][line.index(point)] = 1
    
    return M

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        
        factor = Augmented[i][i]
        for j in range(i, n + 1):
            Augmented[i][j] /= factor
        
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n + 1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Augmented[i][-1]
        for j in range(i + 1, n):
            x[i] -= Augmented[i][j] * x[j]
    
    return x

def discrepancy_method(M):
    m, n = len(M), len(M[0])
    A = [[0] * (n - 1) for _ in range(m)]
    b = [0] * m
    
    for i in range(m):
        for j in range(n - 1):
            A[i][j] = M[i][j]
        b[i] = sum(M[i])
    
    x = gaussian_elimination(A, b)
    discrepancy = max(abs(x[i]) for i in range(n - 1))
    
    return discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2, 3, 4]
    results = []
    
    for q in q_values:
        try:
            points, lines = generate_projective_plane(q)
            M_f = incidence_matrix(points, lines)
            
            D_f = discrepancy_method(M_f)
            metric_value = D_f
            conjecture_holds = abs(D_f - q**2) < 1e-6
            counterexample = "" if conjecture_holds else f"q={q}, D(f)={D_f}"
        except Exception as e:
            metric_value = None
            conjecture_holds = False
            counterexample = str(e)
        
        results.append({
            "metric_name": "discrepancy",
            "metric_value": metric_value,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["trials"])
    
    mean_value = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in all_results if r["metric_value"] is not None) / len(all_results))**0.5
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        counterexample = next(r["counterexample"] for r in all_results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")