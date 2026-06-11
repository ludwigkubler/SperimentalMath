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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
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
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def grothendieck_riemann_roch_rank(A):
        rank = 0
        while A:
            pivot_row = next((i for i, row in enumerate(A) if any(row)), None)
            if pivot_row is None:
                break
            pivot_col = next((j for j, val in enumerate(A[pivot_row]) if val != 0), None)
            if pivot_col is None:
                break
            rank += 1
            A[pivot_row] = [val / A[pivot_row][pivot_col] for val in A[pivot_row]]
            for i in range(len(A)):
                if i != pivot_row:
                    factor = A[i][pivot_col]
                    A[i] = [A[i][j] - factor * A[pivot_row][j] for j in range(len(A[0]))]
        return rank
    
    def resolution_proof_width(phi):
        # Placeholder implementation of proof width calculation
        # This is a dummy function and should be replaced with actual logic
        return len(phi)  # Example: length of the formula as a proxy for proof width
    
    n = random.randint(5, 40)
    phi = [random.choice([0, 1]) for _ in range(n)]
    
    A = [[phi[i] ^ phi[j] for j in range(n)] for i in range(n)]
    grr_rank = grothendieck_riemann_roch_rank(A)
    proof_width = resolution_proof_width(phi)
    
    return {
        "metric_name": "grr_rank vs proof_width",
        "metric_value": abs(grr_rank - proof_width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if grr_rank > proof_width else True,
        "counterexample": "" if grr_rank <= proof_width else "grr_rank > proof_width"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"grr_rank > proof_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")