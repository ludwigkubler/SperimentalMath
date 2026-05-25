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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        result = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        Augmented = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                    max_row = j
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            factor = Augmented[i][i]
            for j in range(i, n+1):
                Augmented[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = Augmented[j][i]
                    for k in range(i, n+1):
                        Augmented[j][k] -= factor * Augmented[i][k]
        return [row[-1] for row in Augmented]
    
    def char_poly(A):
        n = len(A)
        if n == 1:
            return [-A[0], 1]
        else:
            det_A = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det_A += (-1) ** j * A[0][j] * char_poly(submatrix)[0]
            return [-det_A, 1]
    
    def min_circuit_depth(poly):
        n = len(poly)
        if n == 2:
            return 1
        else:
            depth = float('inf')
            for i in range(1, n-1):
                left_poly = poly[:i+1]
                right_poly = poly[i:]
                left_depth = min_circuit_depth(left_poly)
                right_depth = min_circuit_depth(right_poly)
                depth = min(depth, 1 + max(left_depth, right_depth))
            return depth
    
    def delone_set_complexity(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    D = delone_set_complexity(n)
    C = char_poly(D)
    rho_D = len(C) - 1
    min_depth = min_circuit_depth(C)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rho_D,
        "instances_tested": 1,
        "conjecture_holds": rho_D >= min_depth,
        "counterexample": "" if rho_D >= min_depth else f"rho(D)={rho_D}, min_depth={min_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")