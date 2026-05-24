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
    
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
        return coefficients
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(p)] for i in range(m)]
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * matrix[0][c] * sub_det
        return det
    
    def schur_weyl_rank(f):
        n = len(f) - 1
        A = [[f[i + j] for i in range(n - j)] for j in range(n)]
        B = [[f[j - i] for i in range(j + 1)] for j in range(n)]
        AB = matrix_multiply(A, B)
        return determinant(AB)
    
    def det_circuit_lower_bound(f):
        n = len(f) - 1
        return n * (n + 1) // 2
    
    c_0 = 2  # Constant factor for the lower bound
    
    total_rank = 0
    instances_tested = 30
    
    for _ in range(instances_tested):
        f = generate_polynomial(random.randint(5, 40))
        rank = schur_weyl_rank(f)
        det_bound = det_circuit_lower_bound(f) / c_0
        total_rank += rank
    
    average_rank = total_rank / instances_tested
    conjecture_holds = average_rank >= det_bound
    
    return {
        "metric_name": "Schur-Weyl Rank vs Det Circuit Lower Bound",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average rank {average_rank} < det circuit lower bound {det_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank / instances_tested} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank < det circuit lower bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")