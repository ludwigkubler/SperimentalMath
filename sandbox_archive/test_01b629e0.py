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
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
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
    
    def tropical_hodge_norm(A):
        m, n = len(A), len(A[0])
        max_row = [max(row[i] for row in A) for i in range(n)]
        return sum(max_row)
    
    def resolution_length(F):
        # Simplified DPLL solver
        stack = []
        literals = set()
        for clause in F:
            literals.update(clause)
        while stack or literals:
            if not stack and literals:
                literal = random.choice(list(literals))
                stack.append((literal, True))
                literals.remove(literal)
            literal, polarity = stack.pop()
            if polarity:
                literals.discard(-literal)
            else:
                literals.add(-literal)
            for clause in F:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return 1
        return 0
    
    n = random.randint(5, 40)
    F = []
    for _ in range(random.randint(n, 2*n)):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        F.append(clause)
    
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    det_A = determinant(A)
    if det_A == 0:
        return {
            "metric_name": "tropical_hodge_norm",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Determinant of A is zero"
        }
    
    H = tropical_hodge_norm(A)
    k = math.floor(math.log(n, 2))
    expected_length = 2**k / math.log(n)
    
    length = resolution_length(F)
    
    return {
        "metric_name": "tropical_hodge_norm",
        "metric_value": H,
        "instances_tested": 1,
        "conjecture_holds": length >= expected_length,
        "counterexample": "" if length >= expected_length else f"CNF formula requires less than {expected_length} steps"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_length = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean_length = total_length / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction / len(results)}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")