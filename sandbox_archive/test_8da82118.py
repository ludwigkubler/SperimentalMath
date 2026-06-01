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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, n - 1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def hamiltonian_matrix(cnf):
        n = len(cnf[0])
        H = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                if clause[i] != 0:
                    for j in range(i + 1, n):
                        if clause[j] != 0:
                            H[i][j] += Fraction(1)
                            H[j][i] += Fraction(1)
        return H
    
    def min_quaternionic_norm(H):
        n = len(H)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        A = [H[i] + I[i] for i in range(n)]
        B = [I[i] - H[i] for i in range(n)]
        
        def gaussian_elimination(A):
            n = len(A)
            for i in range(n):
                max_row = i
                for k in range(i + 1, n):
                    if abs(A[k][i]) > abs(A[max_row][i]):
                        max_row = k
                A[i], A[max_row] = A[max_row], A[i]
                pivot = A[i][i]
                for j in range(n):
                    A[i][j] /= pivot
                for k in range(n):
                    if k != i:
                        factor = A[k][i]
                        for j in range(n):
                            A[k][j] -= factor * A[i][j]
            return A
        
        A = gaussian_elimination(A)
        B = gaussian_elimination(B)
        
        norm_A = sum(sum(abs(a) for a in row) for row in A)
        norm_B = sum(sum(abs(b) for b in row) for row in B)
        return min(norm_A, norm_B)
    
    def monotone_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, sum(1 for literal in clause if literal != 0))
        return width
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        H = hamiltonian_matrix(cnf)
        norm_H = min_quaternionic_norm(H)
        w_C = monotone_width(cnf)
        results.append((norm_H, w_C))
    
    if not results:
        return {
            "metric_name": "min_quaternionic_norm",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norm_values = [norm for norm, _ in results]
    width_values = [width for _, width in results]
    
    mean_norm = sum(norm_values) / len(norm_values)
    std_norm = math.sqrt(sum((x - mean_norm) ** 2 for x in norm_values) / len(norm_values))
    correlation = sum(norm * width for norm, width in results) / (len(results) * mean_norm * mean_width)
    
    return {
        "metric_name": "min_quaternionic_norm",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")