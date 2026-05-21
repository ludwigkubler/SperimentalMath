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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i == j:
                    A[i][j] = 1
                else:
                    A[i][j] /= A[i][i]
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def max_cut_approximation(A, d):
        n = len(A)
        variables = random.sample(range(n), d)
        cut_value = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j] > 0 and (i in variables) != (j in variables):
                    cut_value += A[i][j]
        return cut_value

    def geometric_entropy(eigenvalues):
        entropy = 0
        for eigenvalue in eigenvalues:
            if eigenvalue > 0:
                entropy -= eigenvalue * math.log2(eigenvalue)
        return entropy

    n = random.randint(5, 40)
    d = random.randint(1, min(n - 1, 10))
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    A = gaussian_elimination(A)
    eigenvalues = [A[i][i] for i in range(n)]
    entropy = geometric_entropy(eigenvalues)
    cut_approximation = max_cut_approximation(A, d)

    return {
        "metric_name": "Geometric Entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= n ** (1 / (d / 2)) and cut_approximation >= 0.878 * sum(eigenvalues),
        "counterexample": "" if entropy <= n ** (1 / (d / 2)) and cut_approximation >= 0.878 * sum(eigenvalues) else f"Entropy: {entropy}, Cut Approximation: {cut_approximation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")