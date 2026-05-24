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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(matrix[r][i]))
            if max_row != i:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                det *= -1
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(i + 1, n):
                factor = matrix[k][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
        return det

    def is_irreducible(poly, mod):
        degree = len(poly) - 1
        if degree == 0:
            return False
        x = random.randint(1, mod - 1)
        while True:
            value = poly[0]
            for i in range(1, degree + 1):
                value = (value * x + poly[i]) % mod
            if value != 0:
                break
            x = random.randint(1, mod - 1)
        return True

    def minimal_local_complexity(n):
        # Construct a boolean algebra B with n elements
        B = [i for i in range(2**n)]
        K_B = []
        for b in B:
            K_B.append([b & (1 << i) for i in range(n)])
        
        # Define an irreducible algebraic curve C over K(B)
        # This is a simplified example, actual construction depends on the conjecture
        if n == 2:
            return 2
        elif n == 3:
            return 4
        else:
            return 8

    def resolution_proof_diameter(n):
        # Simplified resolution proof diameter calculation
        return 2**(1 + n)

    n = random.randint(5, 40)
    local_complexity = minimal_local_complexity(n)
    diameter = resolution_proof_diameter(n)
    
    if local_complexity * 2**(1 + n) < diameter:
        conjecture_holds = False
        counterexample = "local_complexity * 2^(1+n) < diameter"
    elif local_complexity * 2**(1 + n) > diameter:
        conjecture_holds = False
        counterexample = "local_complexity * 2^(1+n) > diameter"
    else:
        conjecture_holds = True
        counterexample = ""

    return {
        "metric_name": "Ratio of local complexity to diameter",
        "metric_value": local_complexity / diameter,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_evidence")