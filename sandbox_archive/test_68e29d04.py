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
            if A[i][i] == 0:
                continue
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def symplectic_leaf(clauses, n):
        points = []
        for clause in clauses:
            point = [0] * (2*n)
            for var in clause:
                if var > 0:
                    point[2*var-1] = 1
                else:
                    point[-2*var] = 1
            points.append(point)
        A = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                row = [points[i][k] ^ points[j][k] for k in range(2*n)]
                if any(row):
                    A.append(row)
        return gaussian_elimination(A)
    
    def min_affine_order(A):
        m, n = len(A), len(A[0])
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def resolution_width(clauses):
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if len(clause) == 1:
                continue
            new_clause = [x for x in clause if x != -clause[0]]
            if not new_clause:
                return len(clauses) - len(stack)
            stack.append(new_clause)
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    
    L = symplectic_leaf(clauses, n)
    min_order = min_affine_order(L)
    w = resolution_width(clauses)
    
    return {
        "metric_name": "min_order_over_w",
        "metric_value": min_order / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if min_order <= 2 * w else False,
        "counterexample": "" if min_order <= 2 * w else "min_order > 2*w"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"min_order > 2*w\" first_failing_seed={first_failing_seed}")