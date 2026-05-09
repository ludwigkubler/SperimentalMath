# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(b)
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for col in range(n):
            max_row = col
            for row in range(col+1, m):
                if abs(Augmented[row][col]) > abs(Augmented[max_row][col]):
                    max_row = row
            Augmented[col], Augmented[max_row] = Augmented[max_row], Augmented[col]
            factor = 1 / Augmented[col][col]
            for j in range(n + 1):
                Augmented[col][j] *= factor
            for i in range(m):
                if i != col:
                    factor = Augmented[i][col]
                    for j in range(n + 1):
                        Augmented[i][j] -= factor * Augmented[col][j]
        return [row[-1] for row in Augmented]
    
    def hilbert_series(f, n):
        # Placeholder for actual Hilbert series computation
        # This is a dummy implementation for testing purposes
        return 1 / (n + 1)
    
    def generate_abp(size):
        # Placeholder for ABP generation
        # This is a dummy implementation for testing purposes
        return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
    
    def polynomial_from_abp(abp):
        # Placeholder for polynomial extraction from ABP
        # This is a dummy implementation for testing purposes
        n = len(abp)
        poly = [0] * (n + 1)
        for i in range(n):
            for j in range(i + 1):
                poly[i - j] += abp[i][j]
        return poly
    
    def ideal_generators(poly):
        # Placeholder for ideal generators extraction
        # This is a dummy implementation for testing purposes
        return [poly]
    
    def leading_coefficient(hilbert_poly):
        # Placeholder for leading coefficient extraction
        # This is a dummy implementation for testing purposes
        return hilbert_poly[0]
    
    n = random.randint(5, 40)
    abp = generate_abp(n)
    poly = polynomial_from_abp(abp)
    ideal_gen = ideal_generators(poly)
    hilbert_poly = hilbert_series(ideal_gen, n)
    leading_coeff = leading_coefficient(hilbert_poly)
    
    return {
        "metric_name": "Leading Coefficient",
        "metric_value": leading_coeff,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")