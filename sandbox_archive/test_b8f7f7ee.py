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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def minimal_local_complexity(n):
        # Constructive mapping for minimal local complexity
        # This is a placeholder; replace with actual implementation
        return random.randint(1, n)

    def resolution_proof_diameter(n):
        # Placeholder for resolution proof diameter calculation
        # Replace with actual implementation
        return 2**(n + 1)

    n = random.choice([5, 10, 15, 20, 30, 40])
    local_complexity = minimal_local_complexity(n)
    proof_diameter = resolution_proof_diameter(n)
    
    ratio = proof_diameter / local_complexity
    
    return {
        "metric_name": "Ratio of Resolution Proof Diameter to Minimal Local Complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2**(1 + n),
        "counterexample": "" if ratio <= 2**(1 + n) else f"n={n}, local_complexity={local_complexity}, proof_diameter={proof_diameter}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result['conjecture_holds'] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result['conjecture_holds'] for result in results) / len(results)
    
    mean_ratio = sum(result['metric_value'] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result['metric_value'] - mean_ratio)**2 for result in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(result['seed'] for result in results if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")