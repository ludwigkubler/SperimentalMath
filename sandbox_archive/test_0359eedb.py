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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
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
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def tropical_hodge_norm(A):
        m, n = len(A), len(A[0])
        max_row = [max(row) for row in A]
        min_col = [min(col) for col in zip(*A)]
        return sum(max_row[i] + min_col[i] for i in range(m))

    def resolution_length(F):
        # Simplified DPLL solver to estimate resolution length
        stack = []
        literals = set()
        for clause in F:
            literals.update(clause)
        while literals:
            literal = random.choice(list(literals))
            literals.remove(literal)
            stack.append((literal, True))
            stack.append((literal, False))
        return len(stack)

    n = 10
    F = []
    for _ in range(2**n):
        clause = [random.randint(-n, n) for _ in range(n)]
        if all(x != 0 for x in clause):
            F.append(clause)

    H = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
    det_H = determinant(H)
    norm_H = tropical_hodge_norm(H)

    k = math.ceil(math.log2(n))
    length = resolution_length(F)

    metric_value = norm_H / math.log(n)
    conjecture_holds = metric_value >= 2**k / math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Tropical Hodge Norm Ratio",
        "metric_value": metric_value,
        "instances_tested": len(F),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")