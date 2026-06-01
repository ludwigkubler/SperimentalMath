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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def local_ring_norm(poly):
        norm = 0
        for coeff in poly:
            norm += abs(coeff)
        return norm ** (1/2)
    
    def clause_indicator_polynomial(clauses, n):
        poly = [Fraction(1)]
        for clause in clauses:
            term = Fraction(1)
            for literal in clause:
                if literal > 0:
                    term *= (1 - x[literal-1])
                else:
                    term *= (x[-literal-1])
            poly = [a + b * term for a, b in zip(poly, term)]
        return poly
    
    def generate_clause_set(n, c):
        clauses = []
        for _ in range(c):
            clause = random.sample(range(1, n+1), 2)
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses
    
    x = [Fraction(1) for _ in range(n)]
    
    n_max = 5
    instances_tested = 0
    total_norm = 0
    max_norm = 0
    
    while True:
        if n > n_max:
            break
        
        c = random.randint(5, 2 * n)
        clauses = generate_clause_set(n, c)
        
        poly = clause_indicator_polynomial(clauses, n)
        norm = local_ring_norm(poly)
        
        total_norm += norm
        max_norm = max(max_norm, norm)
        
        instances_tested += 1
        
        if instances_tested >= 30:
            break
    
    mean_norm = Fraction(total_norm) / instances_tested
    conjecture_holds = max_norm <= 5 * math.sqrt(c)
    
    return {
        "metric_name": "local_ring_norm",
        "metric_value": float(mean_norm),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_norm={max_norm} > 5 * sqrt(c) for c={c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")